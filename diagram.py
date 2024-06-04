from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import Route53, ELB, VPC
from diagrams.aws.security import WAF
from diagrams.aws.compute import ECR, ElasticKubernetesService
from diagrams.aws.database import RDS, RDSInstance
from diagrams.aws.general import User
from diagrams.aws.devtools import Codepipeline, Codebuild
from diagrams.programming.framework import React
from diagrams.programming.language import Nodejs

with Diagram("Complete Architecture", show=False):
    user = User("User")
    developer = User("Developer")

    with Cluster("AWS Cloud"):
        dns = Route53("DNS")
        waf = WAF("Web Application Firewall")
        lb = ELB("Load Balancer")

        with Cluster("Public EKS Cluster"):
            eks_label = ElasticKubernetesService("EKS")
            with Cluster("Web Service 1"):
                frontend1 = React("React Frontend")
                backend1 = Nodejs("Node.js Server")
                frontend1 - Edge(label="") - backend1
            with Cluster("Web Service 2"):
                frontend2 = React("React Frontend")
                backend2 = Nodejs("Node.js Server")
                frontend2 - Edge(label="") - backend2
            with Cluster("Web Service 3"):
                frontend3 = React("React Frontend")
                backend3 = Nodejs("Node.js Server")
                frontend3 - Edge(label="") - backend3

        with Cluster("RDS Cluster"):
            rds_label = RDSInstance("RDS")
            db_primary = RDS("Primary DB")
            db_replicas = [RDS("Replica DB1"), RDS("Replica DB2")]

        dns >> waf >> lb
        lb >> frontend1
        lb >> frontend2
        lb >> frontend3

        backend1 >> db_primary
        backend2 >> db_primary
        backend3 >> db_primary

        db_primary >> db_replicas

        with Cluster("VPC"):
            with Cluster("Development EKS Cluster"):
                dev_eks_label = ElasticKubernetesService("EKS")
                with Cluster("Dev Web Service 1"):
                    dev_frontend1 = React("React Frontend")
                    dev_backend1 = Nodejs("Node.js Server")
                    dev_frontend1 - Edge(label="") - dev_backend1
                with Cluster("Dev Web Service 2"):
                    dev_frontend2 = React("React Frontend")
                    dev_backend2 = Nodejs("Node.js Server")
                    dev_frontend2 - Edge(label="") - dev_backend2
                with Cluster("Dev Web Service 3"):
                    dev_frontend3 = React("React Frontend")
                    dev_backend3 = Nodejs("Node.js Server")
                    dev_frontend3 - Edge(label="") - dev_backend3

            with Cluster("Development RDS Cluster"):
                dev_rds_label = RDSInstance("RDS")
                dev_db_primary = RDS("Dev Primary DB")
                dev_db_replicas = [RDS("Dev Replica DB1"), RDS("Dev Replica DB2")]

            with Cluster("CI/CD Pipeline"):
                code_pipeline = Codepipeline("CodePipeline")
                code_build = Codebuild("CodeBuild")
                ecr = ECR("Elastic Container Registry")

            developer >> code_pipeline >> code_build >> ecr
            ecr >> [dev_backend1, dev_backend2, dev_backend3]
            ecr >> [backend1, backend2, backend3]

            dev_backend1 >> dev_db_primary
            dev_backend2 >> dev_db_primary
            dev_backend3 >> dev_db_primary

            dev_db_primary >> dev_db_replicas

    user >> dns
