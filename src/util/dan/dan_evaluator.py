import argparse
import os
import glob
import networkx as nx
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer, AutoModelForCausalLM
import numpy as np
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_graph(file_path):
    """Loads a DOT file into a NetworkX graph."""
    try:
        import pydot
        
        # Monkeypatch pydot.Dot.get_strict handled for NetworkX compatibility
        # NetworkX 3.2.1 might call get_strict(True), but pydot 4.x only takes self.
        if not hasattr(pydot.Dot, '_original_get_strict'):
            pydot.Dot._original_get_strict = pydot.Dot.get_strict
            def patched_get_strict(self, *args, **kwargs):
                return self._original_get_strict()
            pydot.Dot.get_strict = patched_get_strict

        graphs = pydot.graph_from_dot_file(file_path)
        if not graphs:
            return None
        # Convert the first pydot graph to a NetworkX graph
        return nx.drawing.nx_pydot.from_pydot(graphs[0])
    except Exception as e:
        logger.error(f"Failed to load graph {file_path}: {e}")
        return None

def extract_paths_from_graph(pdg):
    """
    Extracts dependency paths from a PDG.
    Reuses logic from line_extraction.py to find Method/Return nodes.
    """
    source_node = None
    target_node = None
    
    # 1. Find Start (METHOD) and End (METHOD_RETURN) nodes
    for node, data in pdg.nodes(data=True):
        raw_label = str(data.get('label', ''))
        
        # Heuristic: Find the main test method
        # Matches logic in line_extraction.py
        if 'METHOD' in raw_label and 'METHOD_RETURN' not in raw_label:
            # We accept any method that looks like a test method or the main entry point
            # For specific filtering, we might need stricter rules, but we'll take the first viable one per graph for now
            # or try to match the graph name if possible.
            source_node = node
        elif 'METHOD_RETURN' in raw_label:
            target_node = node
            
    if not source_node or not target_node:
        return []

    # 2. Extract paths
    try:
        # Limit to a reasonable number of paths to avoid combinatorial explosion
        # cutoff can be used for length, but all_simple_paths can still be huge.
        # We'll use a generator and slice it.
        paths_generator = nx.all_simple_paths(pdg, source=source_node, target=target_node)
        paths = []
        for i, p in enumerate(paths_generator):
            if i >= 50: # Limit to 50 paths per graph for performance
                break
            paths.append(p)
        return paths
    except nx.NodeNotFound:
        return []
    except Exception as e:
        logger.warning(f"Error extracting paths: {e}")
        return []

def path_to_code_sequence(path, pdg):
    """Converts a list of node IDs to a code string sequence."""
    code_sequence = []
    for node_id in path:
        # Extract label
        raw_label = str(pdg.nodes[node_id].get('label', ''))
        # Simple cleaning: remove HTML-like tags if present, though minimal cleaning is consistent with "raw" code tokens
        # For CodeBERT, raw tokens are usually fine, but let's clean up newlines/quotes slightly
        clean_label = raw_label.replace('\n', ' ').strip()
        code_sequence.append(clean_label)
    return " ".join(code_sequence)

def load_model(model_name):
    """Loads tokenizer and model."""
    logger.info(f"Loading model: {model_name}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        # Check if it's a masked LM (like CodeBERT) or Causal (like CodeLlama)
        # Heuristic: 'bert' or 'roberta' usually MLM
        if 'bert' in model_name.lower() or 'roberta' in model_name.lower():
            model = AutoModelForMaskedLM.from_pretrained(model_name, tie_word_embeddings=False)
            model_type = 'MLM'
        else:
            model = AutoModelForCausalLM.from_pretrained(model_name, tie_word_embeddings=False)
            model_type = 'Causal'
        
        return model, tokenizer, model_type
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return None, None, None

def score_sequence(sequence, model, tokenizer, model_type):
    """
    Computes a score (perplexity/loss) for a sequence.
    Lower score = more natural.
    """
    inputs = tokenizer(sequence, return_tensors="pt", truncation=True, max_length=512)
    
    with torch.no_grad():
        if model_type == 'Causal':
            outputs = model(**inputs, labels=inputs["input_ids"])
            loss = outputs.loss
            return torch.exp(loss).item() # Perplexity
        else:
            # For MLM, pseudo-perplexity is harder. 
            # Simplified approach: Mask tokens one by one? Too slow.
            # Alternative: Just return loss on unmasked input (not ideal for MLM training objective but often used as proxy if MLM head is used)
            # Better: Masked Language Model Scoring (PLL - Pseudo Log-Likelihood)
            # For this script, to keep it fast, we might just use the loss if the model supports calculating loss on labels.
            # CodeBERT is MLM. 
            # A common proxy for MLMs is to evaluate the loss of the sequence.
            # However, HF MLMs often don't compute loss unless labels are provided.
            if 'labels' not in inputs:
                inputs['labels'] = inputs['input_ids'].clone()
            outputs = model(**inputs)
            loss = outputs.loss
            return loss.item() # Just return CrossEntropyLoss

def natural_sort_key(s):
    """Helper for natural sorting (e.g., test_case_9 < test_case_10)."""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def process_directory(directory, model, tokenizer, model_type, limit=None, ordered_files=None):
    """
    Process DOT files in a directory.
    If ordered_files is provided, it must be a list of filenames to process in that order.
    Otherwise, files in the directory are sorted naturally.
    Returns a dict {filename: avg_path_score}.
    """
    scores = {}
    
    if ordered_files:
        files = [os.path.join(directory, f) for f in ordered_files 
                 if os.path.exists(os.path.join(directory, f))]
    else:
        files = glob.glob(os.path.join(directory, "*.dot"))
        files.sort(key=natural_sort_key)

    if limit:
        files = files[:limit]
        
    for f in files:
        basename = os.path.basename(f)
        pdg = load_graph(f)
        if not pdg:
            continue
            
        paths = extract_paths_from_graph(pdg)
        if not paths:
            continue
            
        path_scores = []
        for p in paths:
            seq = path_to_code_sequence(p, pdg)
            s = score_sequence(seq, model, tokenizer, model_type)
            path_scores.append(s)
            
        if path_scores:
            # Average score for this graph (test case)
            avg_score = np.mean(path_scores)
            scores[basename] = avg_score
            logger.info(f"Processed {basename}: Score={avg_score:.4f} ({len(paths)} paths)")
            
    return scores

def main():
    parser = argparse.ArgumentParser(description="DAN Evaluator")
    parser.add_argument("--original_pdg_dir", help="Directory with original PDGs")
    parser.add_argument("--improved_pdg_dir", required=True, help="Directory with improved PDGs")
    parser.add_argument("--model_name", default="microsoft/codebert-base", help="HuggingFace model name")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of files to process")
    
    args = parser.parse_args()
    
    # Load Model
    model, tokenizer, model_type = load_model(args.model_name)
    if not model:
        return

    # Process Improved
    logger.info("Processing Improved Directory...")
    improved_scores = process_directory(args.improved_pdg_dir, model, tokenizer, model_type, args.limit)
    
    original_scores = {}
    if args.original_pdg_dir:
        logger.info("Processing Original Directory...")
        original_scores = process_directory(args.original_pdg_dir, model, tokenizer, model_type, args.limit)
        
    # Stats
    logger.info("-" * 40)
    logger.info("RESULTS")
    logger.info("-" * 40)
    
    # Intersection of files to ensure paired comparison
    common_files = set(improved_scores.keys())
    if args.original_pdg_dir:
        common_files = common_files.intersection(set(original_scores.keys()))
        
    if not common_files:
        logger.warning("No common files found between directories (or only one dir provided).")
        # Just print raw stats for improved
        vals = list(improved_scores.values())
        if vals:
            logger.info(f"Improved: Mean={np.mean(vals):.4f}, Std={np.std(vals):.4f}, N={len(vals)}")
        return

    # Paired Analysis
    if not original_scores:
        logger.info("Improvement statistics skipped (no original directory provided).")
        # Just print raw stats for improved
        vals = list(improved_scores.values())
        if vals:
            logger.info(f"Improved: Mean={np.mean(vals):.4f}, Std={np.std(vals):.4f}, N={len(vals)}")
        return

    org_vals = []
    imp_vals = []
    
    for f in common_files:
        if f not in original_scores:
             continue
        org_vals.append(original_scores[f])
        imp_vals.append(improved_scores[f])
        
    org_mean = np.mean(org_vals)
    imp_mean = np.mean(imp_vals)
    
    logger.info(f"Original Mean Score: {org_mean:.4f}")
    logger.info(f"Improved Mean Score: {imp_mean:.4f}")
    logger.info(f"Difference (Img - Org): {imp_mean - org_mean:.4f}")
    
    # Wilcoxon
    if len(org_vals) > 1:
        try:
            from scipy.stats import wilcoxon
            stat, p_value = wilcoxon(org_vals, imp_vals)
            logger.info(f"Wilcoxon Signed-Rank Test: Statistic={stat}, p-value={p_value:.4e}")
            if p_value < 0.05:
                logger.info("Result is STATISTICALLY SIGNIFICANT.")
            else:
                logger.info("Result is NOT statistically significant.")
        except ImportError:
            logger.info("scipy not installed; skipping Wilcoxon test.")
    else:
        logger.info("Not enough samples for statistical test.")

if __name__ == "__main__":
    main()
