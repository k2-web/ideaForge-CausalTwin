import networkx as nx
import os

class IdeaForgeOntologyGraph:
    def __init__(self, neo4j_uri=None, neo4j_user=None, neo4j_password=None):
        self.graph = nx.DiGraph()
        self.use_neo4j = False
        
        # In-memory backup / main graph initialization
        self._initialize_default_ontology()
        
        # Optional Neo4j connection initialization
        if neo4j_uri and neo4j_user and neo4j_password:
            try:
                from neo4j import GraphDatabase
                self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
                self.use_neo4j = True
                self._sync_to_neo4j()
                print("Successfully connected to Neo4j database.")
            except Exception as e:
                print(f"Failed to connect to Neo4j: {e}. Falling back to in-memory graph.")
                self.use_neo4j = False

    def _initialize_default_ontology(self):
        # 1. Business Segments
        segments = [
            ("Defense_ISR", {"name": "Defense ISR UAVs", "revenue_share": 0.65, "margin_profile": "High margin, lumpy payment cycles"}),
            ("Civil_Mapping", {"name": "Civil Mapping & Surveying", "revenue_share": 0.20, "margin_profile": "Medium margin, competitive tender bidding"}),
            ("FLYGHT_SaaS", {"name": "FLYGHT SaaS Platform", "revenue_share": 0.10, "margin_profile": "High margin recurring, high growth rate"}),
            ("Maintenance_Services", {"name": "Maintenance & Product Support", "revenue_share": 0.05, "margin_profile": "Stable services margin"})
        ]
        for node_id, props in segments:
            self.graph.add_node(node_id, label="BusinessSegment", **props)

        # 2. Product Platforms
        platforms = [
            ("SWITCH_UAV", {"model_name": "SWITCH VTOL UAV", "payload_capacity": "1.2 kg", "flight_endurance": "120 mins", "base_price_lakhs": 25.0}),
            ("NETRA_V4", {"model_name": "NETRA V4 Quadcopter", "payload_capacity": "0.5 kg", "flight_endurance": "45 mins", "base_price_lakhs": 12.0}),
            ("Q6_UAV", {"model_name": "Q6 Heavy Payload UAV", "payload_capacity": "5.0 kg", "flight_endurance": "60 mins", "base_price_lakhs": 35.0}),
            ("FLYGHT_Patrol", {"model_name": "FLYGHT Patrol Software", "payload_capacity": "N/A (SaaS)", "flight_endurance": "N/A", "base_price_lakhs": 1.5})  # Annual subscription
        ]
        for node_id, props in platforms:
            self.graph.add_node(node_id, label="ProductPlatform", **props)

        # 3. Supply Chain Components
        components = [
            ("EO_IR_Optical_Payload", {"type": "Sensor/Payload", "import_dependency": "High (Israel/US)", "lead_time_days": 120, "base_cost_lakhs": 8.0}),
            ("Carbon_Fiber_Frame", {"type": "Structural", "import_dependency": "Medium (Japan)", "lead_time_days": 60, "base_cost_lakhs": 1.5}),
            ("Autopilot_Board", {"type": "Electronics", "import_dependency": "High (Taiwan/Germany)", "lead_time_days": 90, "base_cost_lakhs": 2.0}),
            ("LiPo_Battery_Pack", {"type": "Power", "import_dependency": "Low (Local Assembly)", "lead_time_days": 30, "base_cost_lakhs": 0.8})
        ]
        for node_id, props in components:
            self.graph.add_node(node_id, label="SupplyChainComponent", **props)

        # 4. Government Policies
        policies = [
            ("Drone_PLI_Scheme", {"title": "Drone Production Linked Incentive", "incentive_rate": 0.20, "export_restriction": "None", "impact": "Offsets manufacturing costs"}),
            ("Foreign_Drone_Import_Ban", {"title": "Ban on CBU Drone Imports", "incentive_rate": 0.0, "export_restriction": "None", "impact": "Eliminates foreign competitor drones in India"}),
            ("Defense_Capital_Budget_Allocation", {"title": "MoD Capital Allocation for UAVs", "incentive_rate": 0.0, "export_restriction": "None", "impact": "Determines defense order pipeline volume"})
        ]
        for node_id, props in policies:
            self.graph.add_node(node_id, label="GovernmentPolicy", **props)

        # 5. Customer Entities
        customers = [
            ("Indian_Army", {"category": "Defense", "procurement_channel": "CPPP / Fast Track Procurement"}),
            ("Ministry_of_Home_Affairs", {"category": "Defense / Paramilitary", "procurement_channel": "CPPP / GeM"}),
            ("Survey_of_India_SVAMITVA", {"category": "Civil Government", "procurement_channel": "GeM Tenders"}),
            ("Adani_Ports", {"category": "Commercial Enterprise", "procurement_channel": "Direct Negotiation"})
        ]
        for node_id, props in customers:
            self.graph.add_node(node_id, label="CustomerEntity", **props)

        # 6. Financial Metrics
        metrics = [
            ("Order_Inflow_FY26", {"ind_as_code": "N/A", "quarterly_value": 132.5, "unit": "INR Cr", "desc": "New orders bagged during current quarter"}),
            ("Working_Capital_Days", {"ind_as_code": "Ind AS 107", "quarterly_value": 240.0, "unit": "Days", "desc": "Days taken to convert inventory & receivables to cash"}),
            ("Gross_Margin_Pct", {"ind_as_code": "Ind AS 1", "quarterly_value": 46.5, "unit": "%", "desc": "Gross Profit divided by Revenue"}),
            ("EBITDA_Margin", {"ind_as_code": "Ind AS 1", "quarterly_value": 18.2, "unit": "%", "desc": "Earnings before Interest, Tax, Depreciation, Amortization margin"}),
            ("COGS", {"ind_as_code": "Ind AS 2", "quarterly_value": 65.2, "unit": "INR Cr", "desc": "Cost of Goods Sold (Raw materials + direct labor)"}),
            ("Revenue_FY26", {"ind_as_code": "Ind AS 115", "quarterly_value": 121.8, "unit": "INR Cr", "desc": "Revenue recognized from operations"})
        ]
        for node_id, props in metrics:
            self.graph.add_node(node_id, label="FinancialMetric", **props)

        # Edits / Edges (Relationships)
        edges = [
            # Product Platforms to Business Segments
            ("SWITCH_UAV", "Defense_ISR", {"relationship": "BELONGS_TO"}),
            ("NETRA_V4", "Defense_ISR", {"relationship": "BELONGS_TO"}),
            ("Q6_UAV", "Civil_Mapping", {"relationship": "BELONGS_TO"}),
            ("FLYGHT_Patrol", "FLYGHT_SaaS", {"relationship": "BELONGS_TO"}),

            # Product Platforms to Components
            ("SWITCH_UAV", "EO_IR_Optical_Payload", {"relationship": "REQUIRES_COMPONENT"}),
            ("SWITCH_UAV", "Carbon_Fiber_Frame", {"relationship": "REQUIRES_COMPONENT"}),
            ("SWITCH_UAV", "Autopilot_Board", {"relationship": "REQUIRES_COMPONENT"}),
            ("SWITCH_UAV", "LiPo_Battery_Pack", {"relationship": "REQUIRES_COMPONENT"}),
            
            ("NETRA_V4", "EO_IR_Optical_Payload", {"relationship": "REQUIRES_COMPONENT"}),
            ("NETRA_V4", "Autopilot_Board", {"relationship": "REQUIRES_COMPONENT"}),
            ("NETRA_V4", "LiPo_Battery_Pack", {"relationship": "REQUIRES_COMPONENT"}),

            ("Q6_UAV", "Carbon_Fiber_Frame", {"relationship": "REQUIRES_COMPONENT"}),
            ("Q6_UAV", "Autopilot_Board", {"relationship": "REQUIRES_COMPONENT"}),
            ("Q6_UAV", "LiPo_Battery_Pack", {"relationship": "REQUIRES_COMPONENT"}),

            # Customer Issues Orders to Financial Metrics
            ("Indian_Army", "Order_Inflow_FY26", {"relationship": "ISSUES_ORDER"}),
            ("Ministry_of_Home_Affairs", "Order_Inflow_FY26", {"relationship": "ISSUES_ORDER"}),
            ("Survey_of_India_SVAMITVA", "Order_Inflow_FY26", {"relationship": "ISSUES_ORDER"}),

            # Policies to Components / Metrics
            ("Drone_PLI_Scheme", "Autopilot_Board", {"relationship": "INFLUENCES_COST"}),
            ("Drone_PLI_Scheme", "EBITDA_Margin", {"relationship": "BOOSTS"}),
            ("Foreign_Drone_Import_Ban", "Defense_ISR", {"relationship": "STRENGTHENS_SEGMENT"}),
            ("Defense_Capital_Budget_Allocation", "Order_Inflow_FY26", {"relationship": "DRIVES_DEMAND"}),

            # Supply Chain Components to Financial Metrics
            ("EO_IR_Optical_Payload", "COGS", {"relationship": "DRIVES_COST"}),
            ("Autopilot_Board", "COGS", {"relationship": "DRIVES_COST"}),
            ("Carbon_Fiber_Frame", "COGS", {"relationship": "DRIVES_COST"}),
            ("LiPo_Battery_Pack", "COGS", {"relationship": "DRIVES_COST"}),

            # Financial Flows
            ("Order_Inflow_FY26", "Revenue_FY26", {"relationship": "LEADS_TO_REVENUE"}),
            ("COGS", "Gross_Margin_Pct", {"relationship": "MATHEMATICALLY_REDUCES"}),
            ("Revenue_FY26", "Gross_Margin_Pct", {"relationship": "MATHEMATICALLY_INCREASES"}),
            ("Gross_Margin_Pct", "EBITDA_Margin", {"relationship": "MATHEMATICALLY_FLOWS_TO"}),
            ("Working_Capital_Days", "EBITDA_Margin", {"relationship": "CAUSALLY_IMPACTS"})
        ]
        for src, dest, props in edges:
            self.graph.add_edge(src, dest, **props)

    def _sync_to_neo4j(self):
        # Clears and synchronizes in-memory graph data to the Neo4j instance
        with self.driver.session() as session:
            # Clear database
            session.run("MATCH (n) DETACH DELETE n")
            
            # Create nodes
            for node_id, data in self.graph.nodes(data=True):
                label = data.get("label", "Entity")
                properties = {k: v for k, v in data.items() if k != "label"}
                # Cypher query to create node with variable label
                query = f"CREATE (n:{label} $properties) SET n.id = $node_id"
                session.run(query, properties=properties, node_id=node_id)
            
            # Create relationships
            for u, v, data in self.graph.edges(data=True):
                rel = data.get("relationship", "RELATION")
                query = f"""
                MATCH (a {{id: $u}}), (b {{id: $v}})
                CREATE (a)-[r:{rel}]->(b)
                """
                session.run(query, u=u, v=v)

    def get_nodes(self, class_filter=None):
        nodes_list = []
        for n, data in self.graph.nodes(data=True):
            if class_filter is None or data.get("label") == class_filter:
                nodes_list.append({"id": n, **data})
        return nodes_list

    def get_edges(self):
        edges_list = []
        for u, v, data in self.graph.edges(data=True):
            edges_list.append({"source": u, "target": v, **data})
        return edges_list

    def get_node_details(self, node_id):
        if node_id in self.graph:
            return self.graph.nodes[node_id]
        return None

    def get_2_hop_neighborhood(self, node_id):
        if node_id not in self.graph:
            return {"nodes": [], "edges": []}
        
        # Compute multi-directional 2-hop neighborhood using networkx
        undirected_graph = self.graph.to_undirected()
        neighbors_1 = set(undirected_graph.neighbors(node_id))
        neighbors_2 = set()
        for n in neighbors_1:
            neighbors_2.update(undirected_graph.neighbors(n))
        
        neighborhood_nodes = neighbors_1.union(neighbors_2).union({node_id})
        
        subgraph = self.graph.subgraph(neighborhood_nodes)
        
        nodes_list = [{"id": n, **subgraph.nodes[n]} for n in subgraph.nodes]
        edges_list = [{"source": u, "target": v, **data} for u, v, data in subgraph.edges(data=True)]
        
        return {"nodes": nodes_list, "edges": edges_list}

    def close(self):
        if self.use_neo4j:
            self.driver.close()
