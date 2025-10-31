import json
import os
import re
from pathlib import Path

class SupplyChainDetector:
    SUSPICIOUS_PATTERNS = [
        r'process\.env',
        r'fs\.readFileSync',
        r'https?\.request',
        r'child_process',
        r'eval\(',
        r'Buffer\.from.*toString\([\'"]base64[\'"]\)',
        r'\.npmrc',
        r'AWS_ACCESS_KEY',
        r'DB_PASSWORD'
    ]
    
    RISKY_SCRIPTS = ['postinstall', 'preinstall', 'install']
    
    def __init__(self, package_dir):
        self.package_dir = Path(package_dir)
        self.findings = []
    
    def analyze_package_json(self):
        pkg_path = self.package_dir / 'package.json'
        if not pkg_path.exists():
            return
        
        with open(pkg_path) as f:
            pkg = json.load(f)
        
        scripts = pkg.get('scripts', {})
        for script_name in self.RISKY_SCRIPTS:
            if script_name in scripts:
                self.findings.append({
                    'severity': 'HIGH',
                    'type': 'Risky Install Script',
                    'detail': f'{script_name}: {scripts[script_name]}'
                })
    
    def scan_js_files(self):
        for js_file in self.package_dir.rglob('*.js'):
            try:
                content = js_file.read_text()
                for pattern in self.SUSPICIOUS_PATTERNS:
                    if re.search(pattern, content):
                        self.findings.append({
                            'severity': 'CRITICAL',
                            'type': 'Suspicious Code Pattern',
                            'file': str(js_file.relative_to(self.package_dir)),
                            'pattern': pattern
                        })
            except:
                pass
    
    def report(self):
        print(f"\n🔍 Supply Chain Security Scan: {self.package_dir.name}")
        print("=" * 60)
        
        if not self.findings:
            print("✅ No suspicious patterns detected")
            return
        
        print(f"🚨 Found {len(self.findings)} potential security issues:\n")
        for i, finding in enumerate(self.findings, 1):
            print(f"{i}. [{finding['severity']}] {finding['type']}")
            for k, v in finding.items():
                if k not in ['severity', 'type']:
                    print(f"   {k}: {v}")
            print()

if __name__ == '__main__':
    detector = SupplyChainDetector('supply-chain-attack')
    detector.analyze_package_json()
    detector.scan_js_files()
    detector.report()
