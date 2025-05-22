#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ArgusScan - Advanced Camera Scanner Tool

import requests
import re
import colorama
import os
import time
import argparse
from concurrent.futures import ThreadPoolExecutor
from requests.structures import CaseInsensitiveDict

colorama.init()

# Constants
BASE_URL = "http://www.insecam.org"
COUNTRIES_URL = f"{BASE_URL}/en/jsoncountries/"
HEADERS = CaseInsensitiveDict({
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.insecam.org",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
})

# New ArgusScan Banner
BANNER = """
\033[1;34m

      .o.                                                 .oooooo..o                                 
     .888.                                               d8P'    `Y8                                 
    .8"888.     oooo d8b  .oooooooo oooo  oooo   .oooo.o Y88bo.       .ooooo.   .oooo.   ooo. .oo.   
   .8' `888.    `888""8P 888' `88b  `888  `888  d88(  "8  `"Y8888o.  d88' `"Y8 `P  )88b  `888P"Y88b  
  .88ooo8888.    888     888   888   888   888  `"Y88b.       `"Y88b 888        .oP"888   888   888  
 .8'     `888.   888     `88bod8P'   888   888  o.  )88b oo     .d8P 888   .o8 d8(  888   888   888  
o88o     o8888o d888b    `8oooooo.   `V88V"V8P' 8""888P' 8""88888P'  `Y8bod8P' `Y888""8o o888o o888o 
                         d"     YD                                                                   
                         "Y88888P'                                                                   
                                                                                                 
  \033[1;31mThe All-Seeing Camera Scanner | 100-Eyed Surveillance Tool\033[0m
\033[1;34m
  [*] Named after Argus Panoptes - The Hundred-Eyed Giant [*]
\033[0m
"""

def print_banner():
    """Display the ArgusScan banner"""
    print(BANNER)

def get_countries():
    """Fetch and return the list of countries with camera counts"""
    try:
        resp = requests.get(COUNTRIES_URL, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        return data['countries']
    except Exception as e:
        print(f"\033[1;31mError fetching countries: {e}\033[0m")
        return None

def display_countries(countries):
    """Display available countries with their codes and counts"""
    if not countries:
        return
    
    print("\n\033[1;34mAvailable Countries:\033[0m")
    print("\033[1;32mCode  Country\t\t\tCount\033[0m")
    print("\033[1;32m----  -------\t\t\t-----\033[0m")
    
    for code, info in countries.items():
        print(f"{code}\t{info['country'][:20]:<20}\t{info['count']}")

def get_camera_urls(country_code, max_pages=None, output_file=None):
    """Retrieve camera URLs for a specific country"""
    try:
        url = f"{BASE_URL}/en/bycountry/{country_code}"
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        
        # Extract total pages
        last_page = re.findall(r'pagenavigator\("\?page=", (\d+)', res.text)
        if not last_page:
            print("\033[1;31mNo cameras found for this country.\033[0m")
            return []
            
        last_page = int(last_page[0])
        if max_pages and max_pages < last_page:
            last_page = max_pages
            
        urls = []
        
        # Use threading to speed up fetching multiple pages
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for page in range(last_page + 1):
                futures.append(executor.submit(fetch_page_urls, country_code, page))
            
            for future in futures:
                page_urls = future.result()
                if page_urls:
                    urls.extend(page_urls)
        
        # Save to file if specified
        if output_file:
            save_to_file(urls, output_file)
            
        return urls
        
    except Exception as e:
        print(f"\033[1;31mError retrieving camera URLs: {e}\033[0m")
        return []

def fetch_page_urls(country_code, page):
    """Fetch camera URLs from a specific page"""
    try:
        url = f"{BASE_URL}/en/bycountry/{country_code}/?page={page}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        return re.findall(r"http://\d+\.\d+\.\d+\.\d+:\d+", res.text)
    except Exception as e:
        print(f"\033[1;33mWarning: Error fetching page {page}: {e}\033[0m")
        return []

def save_to_file(urls, filename):
    """Save URLs to a file"""
    try:
        with open(filename, 'w') as f:
            for url in urls:
                f.write(f"{url}\n")
        print(f"\n\033[1;32mSaved {len(urls)} URLs to {filename}\033[0m")
    except Exception as e:
        print(f"\033[1;31mError saving to file: {e}\033[0m")

def check_camera(url, timeout=5):
    """Check if a camera is accessible"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except:
        return False

def main():
    parser = argparse.ArgumentParser(description="Advanced Camera Scanner Tool")
    parser.add_argument('-c', '--country', help="Country code to scan")
    parser.add_argument('-o', '--output', help="Output file name")
    parser.add_argument('-p', '--pages', type=int, help="Maximum pages to scan")
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output")
    parser.add_argument('-t', '--test', action='store_true', help="Test camera accessibility")
    args = parser.parse_args()

    print_banner()
    
    countries = get_countries()
    if not countries:
        return
    
    if not args.country:
        display_countries(countries)
        args.country = input("\n\033[1;36mEnter country code (##): \033[0m")
    
    if args.country not in countries:
        print("\033[1;31mInvalid country code!\033[0m")
        return
    
    output_file = args.output if args.output else f"{args.country}_cameras.txt"
    
    print(f"\n\033[1;35mScanning cameras in {countries[args.country]['country']}...\033[0m")
    
    start_time = time.time()
    urls = get_camera_urls(args.country, args.pages, output_file)
    elapsed_time = time.time() - start_time
    
    if urls:
        print(f"\n\033[1;32mFound {len(urls)} cameras in {elapsed_time:.2f} seconds\033[0m")
        
        if args.test:
            print("\n\033[1;36mTesting camera accessibility...\033[0m")
            accessible = []
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                results = executor.map(check_camera, urls)
                for url, is_accessible in zip(urls, results):
                    if is_accessible:
                        accessible.append(url)
                        if args.verbose:
                            print(f"\033[1;32m[+] {url} - Accessible\033[0m")
                    elif args.verbose:
                        print(f"\033[1;31m[-] {url} - Not accessible\033[0m")
            
            if accessible:
                accessible_file = f"{args.country}_accessible.txt"
                save_to_file(accessible, accessible_file)
                print(f"\n\033[1;32mFound {len(accessible)} accessible cameras\033[0m")
            else:
                print("\033[1;31mNo accessible cameras found\033[0m")
    else:
        print("\033[1;31mNo cameras found for the specified criteria\033[0m")

if __name__ == "__main__":
    main()
