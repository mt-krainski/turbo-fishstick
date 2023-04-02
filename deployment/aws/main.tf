terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  profile = "PowerUserAccess-134105768696"
  region  = "us-east-1"
}

resource "aws_vpc" "my_vpc" {
  cidr_block = "172.31.0.0/16"

  tags = {
    Name = "tf-example"
  }
}

resource "aws_subnet" "my_subnet" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "172.31.10.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "tf-example"
  }
}

resource "aws_network_interface" "foo" {
  subnet_id   = aws_subnet.my_subnet.id
  private_ips = ["172.31.10.100"]

  tags = {
    Name = "primary_network_interface"
  }
}

resource "aws_instance" "test-terraform" {
  ami           = var.ami
  instance_type = var.instance_type

  network_interface {
    network_interface_id = aws_network_interface.foo.id
    device_index         = 0
  }

  credit_specification {
    cpu_credits = "unlimited"
  }
}

variable "ami" {
  type    = string
  default = "ami-006dcf34c09e50022"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}
