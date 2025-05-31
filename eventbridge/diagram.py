from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import Eventbridge
from diagrams.aws.network import APIGateway

with Diagram("Event Processing", show=False, outformat="png", filename="diagram"):
    source = APIGateway("API Gateway source")

    with Cluster("Event Flows"):
        with Cluster("Event Endpoint"):
            workers = [Lambda("worker1")]

        bus = Eventbridge("Event bus")

        with Cluster("Processing"):
            with Cluster("Translate"):
                translate = [Lambda("proc1")]

            with Cluster("Sentiment"):
                sentiment = [Lambda("proc1")]

    source >> workers >> bus
    bus >> translate
    bus >> sentiment
