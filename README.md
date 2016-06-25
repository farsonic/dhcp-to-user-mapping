# dhcp-to-user-mapping
Create entry on SRX User-Authentication-Table mapped from an EX-Series DHCP Server static entry. When this script is executed it will connect to the EX-Series and retreive the static-binding settings from the operational configuration file. The IP-Address and Host-Name are extracted and passed to the SRX as static user-identification entries. 

The script needs to be updated to provide the correct entries for ex/srx hostname (or IP-Address), username and password values. 

Ensure you have the following dependencies installed, pyez, jxmlease and lxml

pip install jxmlease
pip install lxml
pip install junos-eznc

# EX-Series configuration example 
```
set system services dhcp static-binding 92:a2:da:f0:0f:12 fixed-address 192.168.0.130  
set system services dhcp static-binding 92:a2:da:f0:0f:12 host-name Bob_Smith  
set system services dhcp static-binding 10:02:b5:bb:88:f2 fixed-address 192.168.0.131  
set system services dhcp static-binding 10:02:b5:bb:88:f2 host-name Fred_Parker  
```
# SRX-Series

No specific configuration needs to be made on the SRX as it will immediatly begin to populate SYSLOG messages for flow entries based on values in the local user-identification tables. However the firewall policy can enforce individual user restricitions/permissions if required. 

# SRX-Series Operational command
```
admin@vSRX> show security user-identification local-authentication-table all  
Total entries: 2  
Source IP       Username     Roles  
192.168.0.130   Bob_Smith  
192.168.0.131   Fred_Parker  
```
# SRX-Series firewall enforcement (Optional)
```
admin@vSRX> show configuration security policies  
from-zone trust to-zone untrust {  
    policy permitted_user {  
        match {  
            source-address any;  
            destination-address any;  
            application any;  
            source-identity Bob_Smith;  
        }  
        then {  
            permit;  
        }  
    }  
    policy blocked_users {  
        match {  
            source-address any;  
            destination-address any;  
            application any;  
            source-identity Fred_Parker;  
        }  
        then {  
            deny;  
            log {  
                session-close;  
            }  
        }  
    }  
}  
```
