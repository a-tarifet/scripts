# Azure Cleanup Script

This Python script helps you clean up unused resources in your Azure subscription to prevent exceeding your FDPOAzureBudget. It performs the following tasks:

- Scans and deletes unattached Network Interface Cards (NICs)
- Scans and deletes unattached managed disks
- Deletes resources tagged with `cleanup=true`

## Prerequisites

1. Install Python (version 3.x recommended).
2. Install Azure SDK packages:
   ```bash
   pip install azure-identity azure-mgmt-resource azure-mgmt-network azure-mgmt-compute


##How to Use
Clone the repository to your local machine.

Replace the SUBSCRIPTION_ID variable in the script with your Azure Subscription ID.

##Run the script:
python cleanup_script.py

Notes
The script scans for unused resources and prompts for deletion confirmation before proceeding.
Ensure you have the necessary permissions in your Azure subscription.

