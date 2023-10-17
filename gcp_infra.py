import pulumi
import pulumi_gcp as gcp

vertex_network = gcp.compute.get_network(name="default")
vertex_range = gcp.compute.GlobalAddress(
    "vertex-range",
    purpose="VPC_PEERING",
    address_type="INTERNAL",
    prefix_length=24,
    network=vertex_network.id,
)
vertex_vpc_connection = gcp.servicenetworking.Connection(
    "vertexVpcConnection",
    network=vertex_network.id,
    service="servicenetworking.googleapis.com",
    reserved_peering_ranges=[vertex_range.name],
)
project = gcp.organizations.get_project()
endpoint = gcp.vertex.AiEndpoint(
    "endpoint",
    display_name="sample-endpoint",
    description="A sample vertex endpoint",
    location="us-central1",
    region="us-central1",
    network=f"projects/{project.number}/global/networks/{vertex_network.name}",
    opts=pulumi.ResourceOptions(depends_on=[vertex_vpc_connection]),
)
