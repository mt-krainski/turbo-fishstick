terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.21.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "fishstick" {
  name         = "turbo-fishstick:latest"
  keep_locally = false
}

resource "docker_container" "fishstick" {
  image = docker_image.fishstick.image_id
  name  = "turbo-fishstick"
  ports {
    internal = 80
    external = 80
  }
}
