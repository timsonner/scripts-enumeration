import subprocess

def parse_and_lookup(vendor_lookup_url, mac_address):
    cmd_output = subprocess.check_output(['arp', '-a'])
    output = cmd_output.decode('utf-8')
    print(f'ARP command output:\n{output}\n') # Debugging line

    output_lines = output.split('\n')
    for line in output_lines:
        if ' '.join(mac_address.split(':')) in line:
            vendor_mac = line.split()[3]
            print(f'MAC address found: {vendor_mac}\n') # Debugging line
            break
    else:
        print(f'No MAC address found for {mac_address}\n') # Debugging line
        return

    vendor_api_url = vendor_lookup_url + vendor_mac
    print(f'Vendor API URL: {vendor_api_url}\n') # Debugging line

    try:
        cmd_output = subprocess.check_output(['curl', vendor_api_url])
        output = cmd_output.decode('utf-8')
        print(f'API command output:\n{output}\n') # Debugging line

        output_lines = output.split('\n')
        for line in output_lines:
            if 'company' in line:
                vendor = line.split(':')[1].strip()
                print(f'Vendor found: {vendor}\n') # Debugging line
                return
        else:
            print(f'No vendor found for MAC address {vendor_mac}\n') # Debugging line

    except Exception as e:
        print(f'Error occurred during vendor lookup: {e}\n') # Debugging line
        return

if __name__ == '__main__':
    vendor_lookup_url = 'https://api.maclookup.app/v2/macs/'
    mac_address = ''
    parse_and_lookup(vendor_lookup_url, mac_address)
