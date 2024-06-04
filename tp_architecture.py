from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import ELB, VPC, PublicSubnet, PrivateSubnet, InternetGateway
from diagrams.aws.compute import ECR, ElasticKubernetesService
from diagrams.aws.database import RDS
from diagrams.aws.general import User
from diagrams.aws.devtools import Codepipeline, Codebuild
from diagrams.aws.storage import S3
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Ingress
from diagrams.onprem.client import Users
from diagrams.onprem.vcs import Github

with Diagram("Prototype Architecture", show=False, direction="LR"):
    user = Users("User")
    developer = Users("Developer")

    with Cluster("AWS Cloud"):
        igw = InternetGateway("Internet Gateway")

        with Cluster("VPC"):
            vpc = VPC("Main VPC")

            with Cluster("Public Subnet"):
                public_subnet = PublicSubnet("Public Subnet")
                lb = ELB("Load Balancer")
                public_subnet - lb

            with Cluster("Private Subnet"):
                private_subnet = PrivateSubnet("Private Subnet")

                with Cluster("EKS Cluster"):
                    eks = ElasticKubernetesService("EKS")
                    ingress = Ingress("Ingress Controller")

                    with Cluster("Demo App 1"):
                        backend1 = Pod("Node.js Server")

                    with Cluster("Demo App 2"):
                        backend2 = Pod("Node.js Server")

                with Cluster("RDS Instance"):
                    db_primary = RDS("Primary DB")

                lb >> ingress >> [backend1, backend2]
                backend1 >> db_primary
                backend2 >> db_primary

        user >> lb
        vpc - igw

        with Cluster("CI/CD Pipeline"):
            code_pipeline_1 = Codepipeline("CodePipeline App 1")
            code_build_1 = Codebuild("CodeBuild App 1")
            code_pipeline_2 = Codepipeline("CodePipeline App 2")
            code_build_2 = Codebuild("CodeBuild App 2")
            ecr = ECR("Elastic Container Registry")
            s3 = S3("S3 Artifact Store")

    github_repo_1 = Github("Demo App 1 Repo")
    github_repo_2 = Github("Demo App 2 Repo")

    developer >> [github_repo_1, github_repo_2]
    github_repo_1 >> code_pipeline_1 >> code_build_1 >> ecr
    github_repo_2 >> code_pipeline_2 >> code_build_2 >> ecr

    ecr >> [backend1, backend2]
    code_build_1 >> s3
    code_build_2 >> s3
