resource "aws_vpc" "vpc_2" {
  enable_dns_support = true
  cidr_block         = "10.0.0.0/16"

  tags = {
    env      = "Development"
    archUUID = "b4c3f304-ad65-4d84-bb89-df903b81e719"
  }
}

resource "aws_subnet" "subnet_4" {
  vpc_id            = aws_vpc.vpc_2.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-central-1a"

  tags = {
    env      = "Development"
    archUUID = "b4c3f304-ad65-4d84-bb89-df903b81e719"
  }
}

resource "aws_security_group" "security_group_5" {
  vpc_id = aws_vpc.vpc_2.id

  tags = {
    env      = "Development"
    archUUID = "b4c3f304-ad65-4d84-bb89-df903b81e719"
  }
}

resource "aws_instance" "t3a_6" {
  subnet_id         = aws_subnet.subnet_4.id
  availability_zone = "eu-central-1a"

  security_groups = [
    aws_security_group.security_group_5.id,
  ]

  tags = {
    env      = "Development"
    archUUID = "b4c3f304-ad65-4d84-bb89-df903b81e719"
  }
}

