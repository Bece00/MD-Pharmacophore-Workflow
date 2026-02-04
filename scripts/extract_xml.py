import os
import xml.etree.ElementTree as ET
import pandas as pd
import re

# Klasör yolları
results_dir = "plip_results"
all_data = []

# Klasör adından Run ve Frame çekmek için Regex
# run1_frame_3_plip -> Run: 1, Frame: 3
folder_pattern = re.compile(r"run(\d+)_frame_(\d+)")

print("🚀 XML Analizi ve Veri Çekimi Başlıyor...")

if not os.path.exists(results_dir):
    print(f"❌ HATA: '{results_dir}' klasörü bulunamadı!")
    exit()

folders = [f for f in sorted(os.listdir(results_dir)) if os.path.isdir(os.path.join(results_dir, f))]
print(f"📂 Toplam {len(folders)} klasör bulundu. Taranıyor...\n")

for folder in folders:
    folder_path = os.path.join(results_dir, folder)
    # Klasörün içindeki XML dosyasını bul (genelde report.xml)
    xml_files = [f for f in os.listdir(folder_path) if f.endswith(".xml")]
    
    if not xml_files:
        continue
        
    xml_path = os.path.join(folder_path, xml_files[0])
    
    # Run ve Frame bilgisini klasör adından al
    match = folder_pattern.search(folder)
    run_no = match.group(1) if match else "Unknown"
    frame_no = match.group(2) if match else "Unknown"

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Binding Site'ları tara
        for bs in root.findall(".//bindingsite"):
            # Ligand ismini kontrol et (E7M)
            # hetid genelde "E7M" olur
            hetid = bs.find(".//identifiers/hetid")
            if hetid is None or hetid.text != "E7M":
                continue
            
            # --- Etkileşimleri Çek ---
            # 1. Hydrogen Bonds
            for hb in bs.findall(".//hydrogen_bond"):
                all_data.append({
                    "Run": f"Run_{run_no}", "Frame": int(frame_no), "Type": "H-Bond",
                    "Residue": f"{hb.find('restype').text}{hb.find('resnr').text}",
                    "Chain": hb.find('reschain').text,
                    "Dist_DA": float(hb.find('dist_d-a').text),
                    "Angle": float(hb.find('don_angle').text)
                })

            # 2. Hydrophobic
            for hp in bs.findall(".//hydrophobic_interaction"):
                all_data.append({
                    "Run": f"Run_{run_no}", "Frame": int(frame_no), "Type": "Hydrophobic",
                    "Residue": f"{hp.find('restype').text}{hp.find('resnr').text}",
                    "Chain": hp.find('reschain').text,
                    "Distance": float(hp.find('dist').text),
                    "Angle": None
                })

            # 3. Pi-Stacking
            for pi in bs.findall(".//pi_stacking"):
                all_data.append({
                    "Run": f"Run_{run_no}", "Frame": int(frame_no), "Type": "pi-Stacking",
                    "Residue": f"{pi.find('restype').text}{pi.find('resnr').text}",
                    "Chain": pi.find('reschain').text,
                    "Distance": float(pi.find('centdist').text),
                    "Angle": float(pi.find('angle').text)
                })

    except Exception as e:
        print(f"⚠️ {folder} işlenirken hata oluştu: {e}")

# Veriyi DataFrame'e dök ve İstatistik Hesapla
if all_data:
    df = pd.DataFrame(all_data)
    df = df.sort_values(by=["Run", "Frame"])
    
    # Ana listeyi kaydet
    df.to_excel("plip_full_list.xlsx", index=False)
    
    # --- Occupancy (Varlık Yüzdesi) Hesabı ---
    # Toplam frame sayısı (3 run x 1000 frame = 3000 varsayıyoruz)
    total_frames = df['Frame'].nunique() * df['Run'].nunique()
    
    summary = df.groupby(['Residue', 'Type', 'Chain']).size().reset_index(name='Count')
    summary['Occupancy_%'] = (summary['Count'] / total_frames) * 100
    summary = summary.sort_values(by="Occupancy_%", ascending=False)
    
    summary.to_excel("plip_occupancy_summary.xlsx", index=False)
    
    print(f"✅ BAŞARILI: {len(df)} etkileşim satırı işlendi.")
    print(f"📊 Sonuçlar 'plip_full_list.xlsx' ve 'plip_occupancy_summary.xlsx' dosyalarına kaydedildi.")
else:
    print("❌ Hiç PHI1 (E7M) etkileşimi bulunamadı. Lütfen XML içeriğini kontrol et.")