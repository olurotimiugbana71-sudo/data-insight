import sys
from license_gen import LicenseManager

if len(sys.argv) < 3:
    print("Usage: python generate_license.py <email> <tier>")
    sys.exit(1)

lm = LicenseManager()
key = lm.generate_key(sys.argv[1], sys.argv[2])

print(f"""
{'='*50}
  DATAINSIGHT PRO LICENSE
{'='*50}
  Email: {sys.argv[1]}
  Tier: {sys.argv[2]}
  KEY: {key}
{'='*50}
""")