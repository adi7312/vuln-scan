# Script for regular updates of:
# - NVT, SCAP, CERT, GVMD data (threat database)
# - GVM itself
# - Underlying OS

# Update the NVT, SCAP, CERT and GVMD data
greenbone-nvt-sync
greenbone-scapdata-sync
greenbone-certdata-sync
greenbone-feed-sync --type GVMD_DATA
