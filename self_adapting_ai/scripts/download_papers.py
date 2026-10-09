#!/usr/bin/env python3
"""
Research Paper Collector for Self-Adapting AI and Modular Emergence.
Queries arXiv API across domains:
- cs.AI, cs.LG, cs.NE (Neural Evolution / SNNs)
- q-bio.NC (Computational Neuroscience)
- math.OC / math.DS (Dynamical Systems / Optimization)
- cond-mat.dis-nn (Disordered Systems and Neural Networks)
Downloads actual PDFs directly into papers/ directory and extracts metadata.
"""

import os
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json

PAPERS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "papers"))
METADATA_FILE = os.path.join(PAPERS_DIR, "papers_index.json")

os.makedirs(PAPERS_DIR, exist_ok=True)

# Curated high-impact search queries covering the 10-year span (2016-2026) across domains
SEARCH_QUERIES = [
    # Core Transformer architecture & mechanistic circuits
    'ti:"Attention Is All You Need" OR ti:"Transformers" AND cat:cs.LG',
    'ti:"In-context learning" AND ti:"Transformer" AND cat:cs.LG',
    'ti:"Transformer Circuits" OR ti:"Mechanistic Interpretability"',
    # Self-organizing architectures & dynamic rewiring
    'ti:"Self-Organizing" AND ti:"Neural Network" OR ti:"Dynamic Rewiring"',
    'ti:"Synaptic Plasticity" AND ti:"Deep Learning"',
    'ti:"Hebbian" AND ti:"Plasticity" AND ti:"Transformer"',
    # Spiking neural networks & neuroevolution
    'ti:"Spiking Neural" AND ti:"Self-Organizing" OR ti:"STDP"',
    'ti:"Neuroevolution" AND ti:"Architecture" OR ti:"Weight Agnostic"',
    # Modularity emergence & inductive bias
    'ti:"Modularity" AND ti:"Neural Networks" AND ti:"Emergence"',
    'ti:"Localized Learning" OR ti:"Predictive Coding" AND cat:cs.LG',
    # Continuous dynamical systems / Neural ODEs / Liquid nets
    'ti:"Neural Ordinary Differential Equations" OR ti:"Liquid Time-Constant"',
    'ti:"Complex Networks" AND ti:"Self-Organization" AND cat:cond-mat.dis-nn',
    # Hardware & systolic array efficiency
    'ti:"Hardware Lottery" OR ti:"Sparse Neural Networks" AND ti:"Acceleration"'
]

# Specifically targeted landmark papers by ID to guarantee foundational anchors
LANDMARK_ARXIV_IDS = [
    ("1706.03762", "vaswani_2017_attention_is_all_you_need.pdf", "Attention Is All You Need", "cs.CL"),
    ("1906.04358", "gaier_2019_weight_agnostic_neural_networks.pdf", "Weight Agnostic Neural Networks", "cs.LG"),
    ("1806.07366", "chen_2018_neural_ordinary_differential_equations.pdf", "Neural Ordinary Differential Equations", "cs.LG"),
    ("2009.06489", "hooker_2020_the_hardware_lottery.pdf", "The Hardware Lottery", "cs.CY"),
    ("2209.11895", "von_oswald_2022_transformers_learn_in_context_by_gradient_descent.pdf", "Transformers learn in-context by gradient descent", "cs.LG"),
    ("2010.08207", "hasani_2020_liquid_time_constant_networks.pdf", "Liquid Time-Constant Networks", "cs.LG"),
    ("2206.04615", "millidge_2022_predictive_coding_a_review.pdf", "Predictive Coding: A Review", "cs.NE"),
    ("2103.02999", "miconi_2021_hebbian_meta_learning.pdf", "Hebbian Meta-Learning in Deep Networks", "cs.LG"),
    ("2307.02690", "clune_2023_ai_generating_algorithms.pdf", "AI-Generating Algorithms: A New Paradigm for AGI", "cs.AI"),
    ("2309.08586", "kirsch_2023_towards_general_meta_plasticity.pdf", "Towards General Meta-Plasticity", "cs.LG"),
    ("2402.04634", "orchard_2024_self_organizing_circuits.pdf", "Self-Organizing Circuits for Scalable Computing", "cs.NE"),
    ("2404.19756", "liu_2024_kan_kolmogorov_arnold_networks.pdf", "KAN: Kolmogorov-Arnold Networks", "cs.LG"),
]

def download_file(url, target_path):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response, open(target_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def query_arxiv(query, max_results=10):
    base_url = "http://export.arxiv.org/api/query?"
    params = {
        'search_query': query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'relevance',
        'sortOrder': 'descending'
    }
    url = base_url + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': 'SelfAdaptingAI-Research/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
        papers = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            published = entry.find('atom:published', ns).text[:10]
            id_elem = entry.find('atom:id', ns).text
            arxiv_id = id_elem.split('/abs/')[-1]
            pdf_link = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            categories = [c.attrib.get('term') for c in entry.findall('atom:category', ns)]
            papers.append({
                'arxiv_id': arxiv_id,
                'title': title,
                'summary': summary,
                'published': published,
                'pdf_url': pdf_link,
                'categories': categories
            })
        return papers
    except Exception as e:
        print(f"Error querying arXiv for '{query}': {e}")
        return []

def main():
    print("=== Downloading Landmark Research Papers ===")
    all_papers_meta = []
    
    # 1. Download landmark papers first
    for arxiv_id, filename, title, domain in LANDMARK_ARXIV_IDS:
        target_path = os.path.join(PAPERS_DIR, filename)
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        print(f"Fetching landmark: [{arxiv_id}] {title} -> {filename}")
        if not os.path.exists(target_path) or os.path.getsize(target_path) < 1000:
            success = download_file(pdf_url, target_path)
            time.sleep(1)
        else:
            print(f"  Already exists ({os.path.getsize(target_path)} bytes)")
            success = True
        
        all_papers_meta.append({
            'arxiv_id': arxiv_id,
            'filename': filename,
            'title': title,
            'domain': domain,
            'path': target_path,
            'downloaded': success
        })

    # 2. Query arXiv across queries for broader domain coverage
    print("\n=== Querying arXiv across diverse domains ===")
    for q in SEARCH_QUERIES:
        print(f"Querying: {q}")
        papers = query_arxiv(q, max_results=5)
        for p in papers:
            clean_title = "".join(c for c in p['title'][:40] if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
            filename = f"{p['arxiv_id']}_{clean_title}.pdf"
            target_path = os.path.join(PAPERS_DIR, filename)
            if not os.path.exists(target_path) or os.path.getsize(target_path) < 1000:
                print(f"  Downloading: {filename}")
                success = download_file(p['pdf_url'], target_path)
                time.sleep(1.2)  # Respect arXiv API rate limit
            else:
                success = True
            
            p['filename'] = filename
            p['path'] = target_path
            p['downloaded'] = success
            all_papers_meta.append(p)

    # Save index
    with open(METADATA_FILE, 'w') as f:
        json.dump(all_papers_meta, f, indent=2)
    print(f"\nDone! Indexed {len(all_papers_meta)} papers to {METADATA_FILE}")

if __name__ == "__main__":
    main()
