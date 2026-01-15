#!/usr/bin/env python3
"""
Startup Tracker - Find $100M+ funded startups in USA/Europe
"""

import csv
import os
from datetime import datetime

class StartupTracker:
    def __init__(self):
        self.startups = []
        self.min_funding = 100_000_000  # $100M
        self.target_regions = [
            'usa', 'united states', 'us', 'america',
            'europe', 'uk', 'united kingdom', 'germany', 'france', 
            'spain', 'italy', 'netherlands', 'sweden', 'ireland',
            'belgium', 'austria', 'denmark', 'finland', 'norway',
            'switzerland', 'portugal', 'poland'
        ]
    
    def load_manual_data(self, filename='input_data.csv'):
        """Load manually collected startup data from CSV"""
        print(f"\n📂 Loading data from {filename}...")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.startups = list(reader)
            
            print(f"✓ Loaded {len(self.startups)} startups")
            return True
            
        except FileNotFoundError:
            print(f"❌ File '{filename}' not found.")
            print(f"   Please create it using 'input_data_template.csv' as a guide.")
            return False
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def filter_startups(self):
        """Filter startups based on criteria"""
        print("\n🔍 Filtering startups by criteria...")
        print(f"   • Funding >= ${self.min_funding:,}")
        print(f"   • Location: USA or Europe")
        print(f"   • Status: Active")
        print(f"   • IPO Status: Not IPO'd")
        
        filtered = []
        
        for startup in self.startups:
            try:
                # Parse funding amount (handle various formats)
                funding_str = startup.get('funding_amount', '0').replace(',', '').replace('$', '')
                
                # Handle 'M' suffix (e.g., "150M")
                if 'M' in funding_str.upper():
                    funding = float(funding_str.upper().replace('M', '')) * 1_000_000
                elif 'B' in funding_str.upper():
                    funding = float(funding_str.upper().replace('B', '')) * 1_000_000_000
                else:
                    funding = float(funding_str)
                
                location = startup.get('location', '').lower()
                status = startup.get('status', '').lower()
                ipo_status = startup.get('ipo_status', '').lower()
                
                # Check all criteria
                meets_funding = funding >= self.min_funding
                meets_location = any(region in location for region in self.target_regions)
                meets_status = 'active' in status or status == ''
                not_ipod = ipo_status not in ['ipo', 'public', 'listed']
                
                if meets_funding and meets_location and meets_status and not_ipod:
                    startup['funding_amount_parsed'] = f"${funding:,.0f}"
                    filtered.append(startup)
                    
            except (ValueError, TypeError) as e:
                print(f"⚠️  Skipping row due to parsing error: {startup.get('company_name', 'Unknown')}")
                continue
        
        print(f"✓ Found {len(filtered)} startups matching criteria\n")
        return filtered
    
    def export_to_csv(self, filtered_startups, filename='startup_results.csv'):
        """Export filtered results to CSV"""
        if not filtered_startups:
            print("❌ No startups to export")
            return False
        
        print(f"💾 Exporting results to {filename}...")
        
        try:
            # Define output columns
            fieldnames = [
                'company_name', 'funding_amount_parsed', 'location', 
                'status', 'ipo_status', 'funding_round', 
                'description', 'website', 'founded_year'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(filtered_startups)
            
            print(f"✓ Exported {len(filtered_startups)} startups to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting: {e}")
            return False
    
    def display_summary(self, filtered_startups):
        """Display summary statistics"""
        if not filtered_startups:
            return
        
        print("\n" + "="*60)
        print("📊 SUMMARY")
        print("="*60)
        
        # Count by location
        locations = {}
        for startup in filtered_startups:
            loc = startup.get('location', 'Unknown')
            locations[loc] = locations.get(loc, 0) + 1
        
        print(f"\n🌍 Startups by Location:")
        for loc, count in sorted(locations.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {loc}: {count}")
        
        # Top funded
        print(f"\n💰 Top 5 Most Funded:")
        sorted_startups = sorted(
            filtered_startups, 
            key=lambda x: float(x.get('funding_amount_parsed', '$0').replace('$', '').replace(',', '')),
            reverse=True
        )
        
        for i, startup in enumerate(sorted_startups[:5], 1):
            name = startup.get('company_name', 'Unknown')
            funding = startup.get('funding_amount_parsed', '$0')
            location = startup.get('location', 'Unknown')
            print(f"   {i}. {name} - {funding} ({location})")
        
        print("\n" + "="*60 + "\n")

def create_template():
    """Create a template CSV file for manual data entry"""
    template_file = 'input_data_template.csv'
    
    template_data = [
        {
            'company_name': 'Example Startup Inc',
            'funding_amount': '150000000',
            'location': 'San Francisco, USA',
            'status': 'active',
            'ipo_status': 'private',
            'funding_round': 'Series C',
            'description': 'AI-powered analytics platform',
            'website': 'https://example.com',
            'founded_year': '2018'
        },
        {
            'company_name': 'Euro Tech GmbH',
            'funding_amount': '200M',
            'location': 'Berlin, Germany',
            'status': 'active',
            'ipo_status': 'private',
            'funding_round': 'Series D',
            'description': 'Enterprise SaaS solution',
            'website': 'https://eurotech.example',
            'founded_year': '2016'
        }
    ]
    
    with open(template_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = template_data[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(template_data)
    
    print(f"✓ Created template file: {template_file}")
    print(f"  Use this as a guide to create your 'input_data.csv' file\n")

def main():
    print("\n" + "="*60)
    print("🚀 STARTUP TRACKER - $100M+ Funding Finder")
    print("="*60)
    
    tracker = StartupTracker()
    
    # Check if input file exists, if not create template
    if not os.path.exists('input_data.csv'):
        print("\n⚠️  No 'input_data.csv' file found.")
        create_template()
        print("Please add your startup data to 'input_data.csv' and run again.")
        return
    
    # Load data
    if not tracker.load_manual_data('input_data.csv'):
        return
    
    # Filter startups
    filtered_startups = tracker.filter_startups()
    
    if not filtered_startups:
        print("❌ No startups matched your criteria.")
        print("   Try adding more data to input_data.csv")
        return
    
    # Display summary
    tracker.display_summary(filtered_startups)
    
    # Export results
    tracker.export_to_csv(filtered_startups, 'startup_results.csv')
    
    print("✅ Complete! Check 'startup_results.csv' for results.\n")

if __name__ == "__main__":
    main()
