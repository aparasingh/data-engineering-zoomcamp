ssh-keygen -t rsa -f gcp-ssh-key -C apara
passphrase 123

Your identification has been saved in gcp-ssh-key
Your public key has been saved in gcp-ssh-key.pub
The key fingerprint is:
SHA256:kI0OzVkImSCaZw+2kn1sMbQGlgO35tPPA8q1NCKN3DE apara
The key's randomart image is:
+---[RSA 3072]----+
|o.=oo+ ..        |
|.=o+o+.*         |
|o BE* B .        |
|.@.Bo= .         |
|=.B.@ . S        |
| + O *           |
|  o . +          |
|       .         |
|                 |
+----[SHA256]-----+

when you list the contents in .ssh
lists two more files
gcp-ssh-key and .pub of the same
.pub is public key and can be used publicly
don't use other one publicly

Equivalent command of setting up VM:
gcloud compute instances create de-zoomcamp-demo \
    --project=terraform-learn-467211 \
    --zone=europe-west2-a \
    --machine-type=e2-standard-4 \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=285433194102-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
    --create-disk=auto-delete=yes,boot=yes,device-name=de-zoomcamp-demo,image=projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20250722,mode=rw,size=30,type=pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any \
&& \
gcloud compute resource-policies create snapshot-schedule default-schedule-1 \
    --project=terraform-learn-467211 \
    --region=europe-west2 \
    --max-retention-days=14 \
    --on-source-disk-delete=keep-auto-snapshots \
    --daily-schedule \
    --start-time=05:00 \
&& \
gcloud compute disks add-resource-policies de-zoomcamp-demo \
    --project=terraform-learn-467211 \
    --zone=europe-west2-a \
    --resource-policies=projects/terraform-learn-467211/regions/europe-west2/resourcePolicies/default-schedule-1


once the VM is created, note the external IP as that will be used to connect to the VM
IP: 35.234.158.164

htop - to see what type of machine you have


 ~ ssh -i ~/.ssh/gcp-ssh-key apara@35.234.158.164. ---> to run VM

 external IP keeps changing everytime so note it again


 docker run in VM:

 https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md

chmod +x docker-compose -- after installing docker compose to make it executable

