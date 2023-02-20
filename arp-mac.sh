#!/bin/bash

# Function to parse the ARP output and look up the vendor information
parse_and_lookup() {
  vendor_lookup_url="https://api.maclookup.app/v2/macs/"
  mac_address=$1

  # Get ARP output
  cmd_output=$(arp -a)
  echo "ARP command output:"
  echo "$cmd_output"

  # Parse ARP output to find MAC address
  vendor_mac=$(echo "$cmd_output" | grep -i -m 1 "${mac_address}" | awk '{print $4}')
  if [ -z "$vendor_mac" ]; then
    echo "No MAC address found for ${mac_address}"
    return
  fi
  echo "MAC address found: ${vendor_mac}"

  # Look up vendor information using API
  vendor_api_url="${vendor_lookup_url}${vendor_mac}"
  echo "Vendor API URL: ${vendor_api_url}"
  cmd_output=$(curl -s "$vendor_api_url")
  echo "API command output:"
  echo "$cmd_output"
  
  # Parse API output to find vendor information
  vendor=$(echo "$cmd_output" | jq -r '.vendor_details.company_name')
  if [ "$vendor" = "null" ]; then
    echo "No vendor found for MAC address ${vendor_mac}"
    return
  fi
  echo "Vendor found: ${vendor}"
}

# Run the script
parse_and_lookup "$@"
