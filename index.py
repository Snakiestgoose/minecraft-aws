import boto3
import time

# Lambda handler

def handler(event, context):
    # Replace with your EC2 instance ID and key file path
    instance_id = 'i-075d9293848b49666'
    region = 'us-east-2'  # Example region

    # Depending on the incoming event, you can choose to run a variety of commands
    command = event.get('command', 'echo Hello from Lambda!')

    # Provide command validation for allowed commands / usecases
    allowed_commands = ['HelloWorld', 'startInstance', 'stopInstance', 'startMinecraftServer', 'stopMinecraftServer', 'statusMinecraftServer', 'worldBackup']
    if command not in allowed_commands:
        raise ValueError(f"Command '{command}' is not allowed. Allowed commands are: {allowed_commands}")

    # Set the command script based on the command
    command = set_command_script(command)

    # Run the command on the EC2 instance
    try:
        run_command_on_ec2(instance_id, region, command)
    except Exception as e:
        print(f"Error running command on EC2 instance: {e}")
        raise e

def run_command_on_ec2(instance_id, region, command='echo Hello from Lambda!'):

    # If start then validate the instance is running, else if stop then validate the instance is stopped
    if (command == 'startInstance' or command == 'stopInstance'):
        ec2 = boto3.client('ec2', region_name=region)
        if (command == 'startInstance'):
            ec2.start_instances(InstanceIds=[instance_id])
        elif (command == 'stopInstance'):
            ec2.stop_instances(InstanceIds=[instance_id])
    else:
        # create an SSM command to run a bash command on the EC2 instance
        ssm_client = boto3.client('ssm', region_name=region)
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWS-RunShellScript',
            Parameters={'commands': [command]}
        )

        command_id = response['Command']['CommandId']
        print(f"Command sent to instance {instance_id}, command ID: {command_id}")

    
def set_command_script(command):
    # This function can be used to set the command script dynamically
    # For example, you can store it in a database or a file
    # Here we just return the command for simplicity

    if command == 'HelloWorld':
        return 'echo Hello World from EC2!'
    elif command == 'startMinecraftServer':
        return 'screen -dmS minecraft bash -c "cd /opt/minecraft && bash start.sh"'
    elif command == 'stopMinecraftServer':
        # end any active SSM commands
        return 'screen -S minecraft -X quit'
    elif command == 'statusMinecraftServer':
        return 'screen -list | grep minecraft || echo "Minecraft server is not running"'
    elif command == 'worldBackup':
        return (
            'set -e && '
            'backup_date=$(date +%Y%m%d_%H%M%S) && '
            'mkdir -p backups && '
            'zip -r - /opt/minecraft/world | '
            'aws s3 cp - s3://minecraft-mods-442590065328-us-east-2/backups/world_backup_${backup_date}.zip'
        )
    else:
        # Default command if no specific command is matched
        return command
