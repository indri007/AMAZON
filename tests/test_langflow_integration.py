"""
test_langflow_integration.py
Unit tests verifying Langflow Vector Store RAG flow schema and configuration integrity.
"""

import unittest
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

class TestLangflowIntegration(unittest.TestCase):

    def setUp(self):
        self.flow_file = ROOT / "langflow" / "Vector Store RAG.json"

    def test_flow_file_exists_and_valid_json(self):
        self.assertTrue(self.flow_file.exists(), f"{self.flow_file} must exist.")
        with open(self.flow_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)

    def test_flow_contains_data_nodes(self):
        with open(self.flow_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("data", data, "Flow JSON must contain 'data' property")
        flow_data = data["data"]
        self.assertIn("nodes", flow_data, "Flow data must contain 'nodes'")
        nodes = flow_data["nodes"]
        self.assertIsInstance(nodes, list)
        self.assertGreater(len(nodes), 0, "Flow must have at least 1 node")

    def test_flow_contains_rag_components(self):
        with open(self.flow_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        nodes = data["data"]["nodes"]
        node_types = []
        for n in nodes:
            node_data = n.get("data", {})
            node_type = node_data.get("type") or node_data.get("node", {}).get("template", {}).get("_type")
            if node_type:
                node_types.append(str(node_type).lower())
        
        # Check if flow has relevant node types (e.g. prompt, agent, chat, knowledge, or embedding)
        all_text = json.dumps(data).lower()
        self.assertTrue(
            any(k in all_text for k in ["knowledge", "embedding", "agent", "prompt", "chat", "rag"]),
            "Flow must define RAG-related components (knowledge, agent, embedding, or chat)"
        )

if __name__ == "__main__":
    unittest.main()
