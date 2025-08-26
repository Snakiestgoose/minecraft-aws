# minecraft-aws
My Minecraft Server deployed via AWS

## AWS Resources
- EC2 instance with VPC, Security Group, EBS volume, and EIP
- S3 bucket for mods, world data, and world backups
- Lambda for running SSM commands on EC2 instance
- Cloudwatch Agent
- IAM Roles and Policies
- API Gateway

To sync EC2, connect and run: 

- sudo chown ec2-user ./world
- sudo rm ./world/ -r
- sudo aws s3 cp s3://minecraft-mods-{s3-bucket-id}-us-east-2/ServerPack /opt/minecraft --recursive
- sudo aws s3 cp s3://minecraft-mods-{s3-bucket-id}-us-east-2/world /opt/minecraft --recursive
- sudo java -jar fabric-installer.jar


TODO: 
- CloudFormation Update to include all the new changes
- Multi-world commands for Steve-bot and Lambda
- Upgrade to t3.large or t3.xlarge
- Check world status command to work
- Start/Stop checks before starting new screen


## Backup Commands
    set -e && \
    backup_date=$(date +%Y%m%d_%H%M%S) && \
    mkdir -p backups && \
    zip -r backups/world_backup_${backup_date}.zip /opt/minecraft/world && \
    aws s3 cp backups/world_backup_${backup_date}.zip s3://minecraft-mods-{s3-bucket-id}-us-east-2/backups/world_backup_${backup_date}.zip && \
    rm -rf backups/world_backup_${backup_date}.zip

-------------------------
## startMinecraftServer
    screen -dmS minecraft bash -c "cd /opt/minecraft && java -jar fabric-installer.jar"
## stopMinecraftServer
    screen -S minecraft -X quit
## statusMinecraftServer:
    screen -list | grep minecraft || echo "Minecraft server is not running"

--
## Server Update Steps

- Download ServerPack from CurseForge
- Upload zip to s3 bucket like: 
- Copy file to server: 
    - aws s3 cp s3://minecraft-mods-{{account}}-{{region}}/fantasymc_fabric_1.20.1_3.0.0_EXTRA_V2_server_pack/fantasymc_fabric_1.20.1_3.0.0_EXTRA_V2_server_pack.zip /serverpacks
- Unzip and replace files
    - unzip -o serverpacks/fantasymc_fabric_1.21.1_0.2.3.5_server_pack.zip -d /opt/minecraft/
- Udpate to matching jar 
    - wget https://meta.fabricmc.net/v2/versions/loader/1.20.1/0.16.13/1.0.3/server/jar -O /opt/minecraft/fabric-installer.jar
- Initial Run
    - java -jar fabric-installer.jar


sudo wget https://meta.fabricmc.net/v2/versions/loader/1.20.1/0.16.10/1.0.3/server/jar -O /opt/minecraft/fabric-installer
unzip -o serverpacks/FantasyMC-ServerPack-v14.0.zip -d /opt/minecraft/
sudo unzip -o world_backup_20250628_155113.zip -d /
SEED: [-5626600480586320944]
sudo rm -rf ./*

Biome makeover
supplementaries