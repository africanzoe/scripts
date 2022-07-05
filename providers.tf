terraform {
  required_providers {
    aws = {
      version = "= 4.8.0"
    }
  }
}

provider "aws" {
  # This region will be calculated automatically based on the design
  region = "eu-central-1"

  # write your custom provider settings here

}

