
terraform {
  backend "s3" {
    bucket = "security-topologies"
    key    = "b4c3f304-ad65-4d84-bb89-df903b81e719"
    region = "eu-west-3"
  }
}
  