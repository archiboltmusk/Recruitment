import json
from typing import List, Dict, Any

EXAMS_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "upsc-cms-2026-paper-1-authentic",
        "title": "UPSC CMS 2026 Official Paper-I (Authentic PYQ Set)",
        "subtitle": "Complete 120 Qs • Official Booklet T.B.C. NTDC-O-KPMS (General Medicine & Pediatrics + X-Ray)",
        "total_questions": 120,
        "total_marks": 250,
        "duration_minutes": 120,
        "negative_marking": 0.33,
        "subjects": ["General Medicine", "Pediatrics"],
        "year": "2026 Official UPSC Paper",
        "difficulty": "Authentic UPSC Standard",
        "cutoff_reference": 130
    },
    {
        "id": "upsc-cms-2026-paper-2-authentic",
        "title": "UPSC CMS 2026 Official Paper-II (Authentic PYQ Set)",
        "subtitle": "Complete 120 Qs • Official Booklet T.B.C. NTDC-T-GSPO (Surgery, OBG & PSM + 9 Image Questions)",
        "total_questions": 120,
        "total_marks": 250,
        "duration_minutes": 120,
        "negative_marking": 0.33,
        "subjects": ["General Surgery", "Obstetrics & Gynaecology", "Preventive & Social Medicine"],
        "year": "2026 Official UPSC Paper",
        "difficulty": "Authentic UPSC Standard",
        "cutoff_reference": 132
    },
    {
        "id": "upsc-cms-paper-1",
        "title": "UPSC Combined Medical Services (CMS) — Paper 1",
        "subtitle": "General Medicine (96 Qs) & Pediatrics (24 Qs)",
        "total_questions": 12,
        "total_marks": 250,
        "duration_minutes": 120,
        "negative_marking": 0.33,
        "subjects": ["General Medicine", "Pediatrics"],
        "year": "2024 Official Pattern",
        "difficulty": "Medium to High (Clinical Scenarios)",
        "cutoff_reference": 128
    },
    {
        "id": "upsc-cms-paper-2",
        "title": "UPSC Combined Medical Services (CMS) — Paper 2",
        "subtitle": "Surgery (40 Qs), OBG (40 Qs), and PSM (40 Qs)",
        "total_questions": 12,
        "total_marks": 250,
        "duration_minutes": 120,
        "negative_marking": 0.33,
        "subjects": ["General Surgery", "Obstetrics & Gynaecology", "Preventive & Social Medicine"],
        "year": "2024 Official Pattern",
        "difficulty": "Medium to High",
        "cutoff_reference": 132
    },
    {
        "id": "cms-clinical-pharma",
        "title": "Clinical Pharmacology & Antimicrobial Stewardship Drill",
        "subtitle": "High-Yield Antibiotics, Toxicities, and Emergency Antidotes",
        "total_questions": 6,
        "total_marks": 100,
        "duration_minutes": 45,
        "negative_marking": 0.33,
        "subjects": ["Clinical Pharmacology"],
        "year": "2024 High-Yield",
        "difficulty": "Moderate",
        "cutoff_reference": 60
    },
    {
        "id": "cms-psm-national-programs",
        "title": "National Health Programs & Epidemiology Vault",
        "subtitle": "NTEP (TB), UIP (Vaccines), NVBDCP, and Demography Indices",
        "total_questions": 6,
        "total_marks": 100,
        "duration_minutes": 45,
        "negative_marking": 0.33,
        "subjects": ["Preventive & Social Medicine"],
        "year": "2024 High-Yield",
        "difficulty": "Moderate",
        "cutoff_reference": 65
    },
    {
        "id": "esic-imo-clinical-drill",
        "title": "ESIC Insurance Medical Officer (IMO) High-Yield Drill",
        "subtitle": "Clinical Outpatient & Emergency Medicine Scenarios",
        "total_questions": 10,
        "total_marks": 100,
        "duration_minutes": 60,
        "negative_marking": 0.25,
        "subjects": ["Emergency Medicine", "Pharmacology", "General Medicine"],
        "year": "2023-2024 Cadre",
        "difficulty": "Standard Clinical",
        "cutoff_reference": 65
    }
]

EXAM_QUESTIONS: Dict[str, List[Dict[str, Any]]] = {
    "upsc-cms-paper-1": [
        {
            "id": "cms1-01",
            "subject": "General Medicine",
            "text": "A 58-year-old male with a history of long-standing hypertension presents with sudden onset retrosternal chest pain radiating to the interscapular region. Blood pressure is 186/110 mmHg in the right arm and 142/86 mmHg in the left arm. A grade II early diastolic decrescendo murmur is heard at the right sternal border. What is the most sensitive and initial diagnostic modality of choice in this hemodynamically stable patient?",
            "options": [
                "Transthoracic Echocardiogram (TTE)",
                "CT Angiography of the Chest with IV contrast",
                "Magnetic Resonance Angiography (MRA)",
                "Standard 12-lead ECG and Troponin I serial levels"
            ],
            "correct_option": 1,
            "explanation": "The clinical presentation (severe tearing chest pain radiating to back, asymmetric arm BP >20 mmHg, and new aortic regurgitation murmur) is classic for Acute Aortic Dissection (Stanford Type A). In a hemodynamically stable patient, CT Angiography of the chest is the most sensitive (98-100%) and preferred initial investigation of choice. In unstable patients, Transesophageal Echocardiography (TEE) or bedside TTE is preferred.",
            "citation": "Harrison's Principles of Internal Medicine, 21st Edition, Chapter 274: Diseases of the Aorta"
        },
        {
            "id": "cms1-02",
            "subject": "General Medicine",
            "text": "A 42-year-old female presents with persistent fatigue, cold intolerance, and constipation. Laboratory investigations reveal: TSH = 18.4 mIU/L (Normal: 0.4–4.0), Free T4 = 0.5 ng/dL (Normal: 0.8–1.8), and elevated anti-Thyroperoxidase (anti-TPO) antibodies. What is the standard starting dose of Levothyroxine for this patient with primary overt hypothyroidism?",
            "options": [
                "12.5 mcg daily",
                "25 mcg daily",
                "1.6 mcg/kg body weight daily",
                "100 mcg twice weekly"
            ],
            "correct_option": 2,
            "explanation": "In young to middle-aged patients without underlying coronary artery disease or cardiac arrhythmias, the full replacement dose of Levothyroxine is approximately 1.6 mcg/kg/day taken orally on an empty stomach 30-60 minutes before breakfast. In elderly patients or those with ischemic heart disease, treatment is started low (12.5–25 mcg/day) and titrated gradually.",
            "citation": "Harrison's Endocrinology, 4th Edition, Chapter on Hypothyroidism"
        },
        {
            "id": "cms1-03",
            "subject": "General Medicine",
            "text": "In a patient presenting with Diabetic Ketoacidosis (DKA) with Blood Glucose = 440 mg/dL, pH = 7.18, Serum Potassium = 3.1 mEq/L, and Urine Ketones +++, which of the following is the CORRECT immediate therapeutic priority?",
            "options": [
                "Start IV Regular Insulin bolus (0.1 units/kg) immediately",
                "Start aggressive IV 0.9% Normal Saline hydration and IV Potassium replacement BEFORE administering insulin",
                "Administer IV Sodium Bicarbonate infusion immediately",
                "Administer IV 5% Dextrose infusion"
            ],
            "correct_option": 1,
            "explanation": "CRITICAL EMERGENCY PROTOCOL: If serum potassium is < 3.3 mEq/L in DKA, insulin administration MUST BE WITHHELD while IV fluid resuscitation and potassium repletion (20-30 mEq/hr) are initiated. Giving insulin immediately would drive potassium into cells and precipitate life-threatening cardiac arrhythmias, respiratory muscle paralysis, or cardiac arrest.",
            "citation": "ADA Standards of Medical Care in Diabetes; Harrison's Principles of Internal Medicine"
        },
        {
            "id": "cms1-04",
            "subject": "General Medicine",
            "text": "A 35-year-old male from an endemic area presents with high fever with rigors occurring every alternate day, severe headache, and splenomegaly. Peripheral blood smear confirms Plasmodium vivax infection. Which drug is mandatory to prevent relapses by eradicating dormant hypnozoites in the liver, provided the patient is not G6PD deficient?",
            "options": [
                "Chloroquine for 3 days",
                "Primaquine 0.25 mg/kg daily for 14 days",
                "Artesunate plus Lumefantrine",
                "Doxycycline 100 mg twice daily for 7 days"
            ],
            "correct_option": 1,
            "explanation": "For radical cure of Plasmodium vivax and Plasmodium ovale malaria, Chloroquine or ACT clears the blood-stage schizonts, but Primaquine (0.25 mg/kg/day for 14 days) is essential to eradicate the persistent exoerythrocytic hypnozoites in the liver. G6PD status must be verified before prescribing Primaquine to avoid severe hemolytic anemia.",
            "citation": "NVBDCP National Drug Policy on Malaria; Harrison's Infectious Diseases"
        },
        {
            "id": "cms1-05",
            "subject": "Pediatrics",
            "text": "According to the National Immunization Schedule (NIS) of India, what is the correct age of administration for the first dose of the Measles-Rubella (MR) vaccine along with Vitamin A supplementation?",
            "options": [
                "At 6 weeks of age",
                "At 9 completed months to 12 months",
                "At 14 weeks of age",
                "At 16 to 24 months of age"
            ],
            "correct_option": 1,
            "explanation": "Under the Universal Immunization Programme (UIP) of India, MR 1st dose (0.5 mL subcutaneous in right upper arm) is administered upon completion of 9 months up to 12 months, accompanied by the 1st dose of Vitamin A (100,000 IU orally). The 2nd MR dose is given at 16-24 months with 200,000 IU Vitamin A.",
            "citation": "OP Ghai Essential Pediatrics, 9th Edition; MoHFW Universal Immunization Guidelines"
        },
        {
            "id": "cms1-06",
            "subject": "Pediatrics",
            "text": "A 2-year-old child presents with severe generalized bilateral pitting edema, moon face, sparse hypopigmented hair with 'flag sign', and apathy. Appetite is poor and weight-for-height Z-score is -2.5 SD. This presentation is most characteristic of which form of Severe Acute Malnutrition (SAM)?",
            "options": [
                "Marasmus",
                "Kwashiorkor (Edematous Malnutrition)",
                "Nutritional Rickets",
                "Congenital Nephrotic Syndrome"
            ],
            "correct_option": 1,
            "explanation": "Kwashiorkor is characterized by bilateral pedal/generalized pitting edema, preserved subcutaneous fat, hepatomegaly due to fatty infiltration, 'flag sign' (alternating bands of dark and light hair), and psychiatric changes (apathy and irritability). Marasmus, by contrast, presents with severe muscle wasting, absent subcutaneous fat, 'old man facies', and an alert, voracious appetite without edema.",
            "citation": "WHO Guidelines on Severe Acute Malnutrition; Ghai Essential Pediatrics"
        },
        {
            "id": "cms1-07",
            "subject": "General Medicine",
            "text": "Which of the following is the hallmark finding on bone marrow aspiration that confirms a diagnosis of Visceral Leishmaniasis (Kala-Azar)?",
            "options": [
                "Presence of amastigotes (Leishman-Donovan bodies) inside macrophages",
                "Flagellated promastigotes in extracellular fluid",
                "Reed-Sternberg giant cells",
                "Auer rods in myeloblasts"
            ],
            "correct_option": 0,
            "explanation": "Demonstration of Leishman-Donovan (LD) bodies—which are the intracellular, non-flagellated amastigote form of Leishmania donovani inside reticuloendothelial macrophages—in bone marrow or splenic aspirate smears confirms Kala-Azar. The flagellated promastigote form is found only in the gut of the sandfly vector (Phlebotomus argentipes) or in culture.",
            "citation": "Harrison's Principles of Internal Medicine; Park's Textbook of Preventive and Social Medicine"
        },
        {
            "id": "cms1-08",
            "subject": "General Medicine",
            "text": "A 65-year-old male with chronic COPD presents to casualty with acute exacerbation. Arterial Blood Gas (ABG) analysis shows: pH = 7.24, PaCO2 = 68 mmHg, PaO2 = 54 mmHg, HCO3 = 28 mEq/L. What is the primary acid-base disturbance?",
            "options": [
                "Metabolic Acidosis with respiratory compensation",
                "Acute on Chronic Respiratory Acidosis",
                "Uncompensated Respiratory Alkalosis",
                "Mixed Metabolic and Respiratory Alkalosis"
            ],
            "correct_option": 1,
            "explanation": "pH < 7.35 indicates acidosis. Elevated PaCO2 (>45 mmHg) confirms respiratory acidosis. The elevated bicarbonate (28 mEq/L) represents chronic renal compensation for longstanding CO2 retention, but the low pH indicates acute worsening (decompensation), making this an Acute on Chronic Respiratory Acidosis.",
            "citation": "Harrison's Principles of Internal Medicine, Chapter: Acidosis and Alkalosis"
        },
        {
            "id": "cms1-09",
            "subject": "Pediatrics",
            "text": "An 18-month-old child presents with a barking cough, inspiratory stridor, and hoarseness of voice that worsens at night. An anteroposterior soft tissue neck radiograph reveals the classic 'Steeple Sign' (subglottic narrowing). What is the primary etiology and drug of choice?",
            "options": [
                "Bacterial tracheitis; IV Vancomycin",
                "Croup (Laryngotracheobronchitis) caused by Parainfluenza virus; Oral Dexamethasone",
                "Acute Epiglottitis caused by Hib; IV Ceftriaxone",
                "Foreign body aspiration; Rigid bronchoscopy"
            ],
            "correct_option": 1,
            "explanation": "The clinical triad of barking 'seal-like' cough, inspiratory stridor, and hoarseness with the radiological 'Steeple sign' confirms Croup (Acute Laryngotracheobronchitis), most commonly caused by Human Parainfluenza virus type 1. Oral single-dose Dexamethasone (0.15–0.6 mg/kg) is the cornerstone treatment, supplemented with nebulized L-epinephrine in severe respiratory distress.",
            "citation": "Nelson Textbook of Pediatrics, 21st Edition; Ghai Essential Pediatrics"
        },
        {
            "id": "cms1-10",
            "subject": "General Medicine",
            "text": "Which drug is recognized as the first-line disease-modifying antirheumatic drug (DMARD) of choice for initial therapy in Rheumatoid Arthritis?",
            "options": [
                "Hydroxychloroquine",
                "Methotrexate",
                "Infliximab",
                "Sulfasalazine"
            ],
            "correct_option": 1,
            "explanation": "Methotrexate (starting at 7.5 to 15 mg once weekly orally along with Folic acid supplementation) is universally recognized by ACR and EULAR as the anchor first-line conventional synthetic DMARD for active rheumatoid arthritis.",
            "citation": "Harrison's Rheumatology; ACR Guidelines for Management of Rheumatoid Arthritis"
        },
        {
            "id": "cms1-11",
            "subject": "General Medicine",
            "text": "A 24-year-old medical intern sustains an accidental needle-stick injury while drawing blood from an HIV-positive patient with high viral load. Post-Exposure Prophylaxis (PEP) should ideally be initiated within how many hours of exposure?",
            "options": [
                "Within 2 hours (and not later than 72 hours)",
                "Within 7 days",
                "Within 14 days",
                "Only if antibody tests turn positive at 6 weeks"
            ],
            "correct_option": 0,
            "explanation": "According to NACO and WHO guidelines, Post-Exposure Prophylaxis (PEP) for HIV should be initiated as soon as possible, ideally within 2 hours, and no later than 72 hours post-exposure. Standard PEP regimen consists of a 28-day course of triple antiretroviral therapy (e.g. Tenofovir + Lamivudine + Dolutegravir).",
            "citation": "NACO National Guidelines for Post-Exposure Prophylaxis, MoHFW"
        },
        {
            "id": "cms1-12",
            "subject": "Pediatrics",
            "text": "A neonate is evaluated at 1 minute and 5 minutes after birth. At 5 minutes: Heart rate = 110 bpm, Respiration = strong cry, Muscle tone = active motion and well-flexed extremities, Reflex irritability = vigorous cry on stimulation, Color = body pink with blue extremities (acrocyanosis). What is the Apgar score?",
            "options": [
                "10",
                "9",
                "8",
                "7"
            ],
            "correct_option": 1,
            "explanation": "Apgar components: Heart rate > 100 bpm = 2; Respiration (strong cry) = 2; Muscle tone (active motion) = 2; Reflex irritability (vigorous cry) = 2; Color (acrocyanosis / pink body with blue hands/feet) = 1. Total score = 2 + 2 + 2 + 2 + 1 = 9.",
            "citation": "Nelson Textbook of Pediatrics; Ghai Essential Pediatrics"
        }
    ],

    "upsc-cms-paper-2": [
        {
            "id": "cms2-01",
            "subject": "General Surgery",
            "text": "A 28-year-old male presents with periumbilical colicky abdominal pain that shifts to the right lower quadrant after 8 hours. On examination, localized tenderness, guarding, and rebound tenderness are noted at McBurney's point. Rovsing's sign and Psoas sign are positive. What is the most appropriate management?",
            "options": [
                "Empiric oral antibiotics and observation for 48 hours",
                "Immediate Appendectomy (Laparoscopic or Open)",
                "Barium Enema examination",
                "Colonoscopy with mucosal biopsy"
            ],
            "correct_option": 1,
            "explanation": "The shifting of pain (visceral to somatic) with signs of localized peritoneal inflammation at McBurney's point is hallmark for Acute Appendicitis. Early surgical intervention (Appendectomy) remains the definitive gold standard to prevent perforation, gangrene, and peritonitis.",
            "citation": "Bailey & Love's Short Practice of Surgery, 28th Edition, Chapter on The Vermiform Appendix"
        },
        {
            "id": "cms2-02",
            "subject": "General Surgery",
            "text": "Which anatomical structure forms the inferior boundary of the Calot's Triangle (Hepatocystic Triangle), an essential landmark in Laparoscopic Cholecystectomy?",
            "options": [
                "Common Hepatic Duct",
                "Cystic Duct",
                "Inferior border of liver",
                "Cystic Artery"
            ],
            "correct_option": 1,
            "explanation": "Anatomy of Calot's (Hepatocystic) triangle: Medial border = Common Hepatic Duct; Inferior/Lateral border = Cystic Duct; Superior border = Inferior surface of liver segment V. The triangle contains the Cystic Artery and Lund's lymph node.",
            "citation": "Bailey & Love's Short Practice of Surgery; Fischer's Mastery of Surgery"
        },
        {
            "id": "cms2-03",
            "subject": "Obstetrics & Gynaecology",
            "text": "A 32-week pregnant primigravida presents with headache, scotoma, and blood pressure of 166/112 mmHg recorded on two occasions 4 hours apart. Urine dipstick shows +++ proteinuria. What is the anticonvulsant drug of choice to prevent and treat eclamptic seizures?",
            "options": [
                "IV Diazepam",
                "IV Phenytoin",
                "Magnesium Sulphate (Pritchard or Zuspan regimen)",
                "Oral Levetiracetam"
            ],
            "correct_option": 2,
            "explanation": "Magnesium Sulphate is the proven drug of choice worldwide (confirmed by the landmark Collaborative Eclampsia Trial) for prevention and control of seizures in severe pre-eclampsia and eclampsia. Pritchard regimen involves 4g IV + 10g IM loading dose, followed by 5g IM maintenance dose every 4 hours.",
            "citation": "DC Dutta's Textbook of Obstetrics, 9th Edition; Williams Obstetrics"
        },
        {
            "id": "cms2-04",
            "subject": "Obstetrics & Gynaecology",
            "text": "What is the defining criterion for Postpartum Hemorrhage (PPH) following a normal vaginal delivery according to WHO guidelines?",
            "options": [
                "Blood loss exceeding 200 mL within 24 hours",
                "Blood loss exceeding 500 mL within 24 hours",
                "Blood loss exceeding 1000 mL within 24 hours",
                "Any blood loss that causes a hemoglobin drop of 1 g/dL"
            ],
            "correct_option": 1,
            "explanation": "According to WHO, Postpartum Hemorrhage (PPH) is defined as blood loss of 500 mL or more within 24 hours after vaginal birth, or 1000 mL or more after cesarean section. Uterine atony is responsible for ~80% of primary PPH cases.",
            "citation": "WHO Recommendations for the Prevention and Treatment of Postpartum Haemorrhage; DC Dutta's Obstetrics"
        },
        {
            "id": "cms2-05",
            "subject": "Preventive & Social Medicine",
            "text": "In epidemiological screening, the ability of a diagnostic test to correctly identify all those who truly have the disease is defined as:",
            "options": [
                "Specificity",
                "Sensitivity",
                "Positive Predictive Value",
                "Negative Predictive Value"
            ],
            "correct_option": 1,
            "explanation": "Sensitivity is the true positive rate: the probability that a test is positive given that the patient has the disease [TP / (TP + FN)]. Specificity is the true negative rate: the probability that a test is negative in a disease-free individual [TN / (TN + FP)].",
            "citation": "Park's Textbook of Preventive and Social Medicine, 26th Edition, Chapter on Screening for Disease"
        },
        {
            "id": "cms2-06",
            "subject": "Preventive & Social Medicine",
            "text": "What is the primary vector responsible for the transmission of Dengue and Chikungunya viruses in urban Indian environments?",
            "options": [
                "Anopheles stephensi",
                "Culex quinquefasciatus",
                "Aedes aegypti",
                "Mansonia annulifera"
            ],
            "correct_option": 2,
            "explanation": "Aedes aegypti (tiger mosquito) is the primary daytime-biting domestic vector for Dengue, Chikungunya, and Zika. It breeds in clean, artificial collections of stagnant water (air coolers, discarded tyres, overhead cisterns).",
            "citation": "Park's Textbook of Preventive and Social Medicine; NVBDCP Guidelines"
        },
        {
            "id": "cms2-07",
            "subject": "General Surgery",
            "text": "According to the Parkland Formula, what is the total crystalloid fluid requirement in the first 24 hours for a 70 kg adult patient suffering from 40% second-degree thermal burns?",
            "options": [
                "5,600 mL",
                "11,200 mL (with half given in first 8 hours)",
                "8,400 mL",
                "14,000 mL"
            ],
            "correct_option": 1,
            "explanation": "Parkland Formula: Total Fluid (Ringer's Lactate) = 4 mL × Body weight in kg × % TBSA burn = 4 × 70 × 40 = 11,200 mL. Half (5,600 mL) must be infused in the first 8 hours from the TIME OF INJURY, and the remaining half over the subsequent 16 hours.",
            "citation": "Bailey & Love's Short Practice of Surgery, Chapter on Burns; ATLS Manual"
        },
        {
            "id": "cms2-08",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which of the following is the most common cause of early recurrent spontaneous pregnancy loss (recurrent miscarriage) in the first trimester?",
            "options": [
                "Fetal chromosomal abnormalities (Aneuploidy)",
                "Cervical incompetence",
                "Uncontrolled gestational diabetes",
                "Bicornuate uterus"
            ],
            "correct_option": 0,
            "explanation": "Chromosomal anomalies (aneuploidies like autosomal trisomies, monosomy X, and triploidy) account for 50-70% of all spontaneous first-trimester miscarriages. Anatomical factors like cervical incompetence typically cause painless mid-trimester (second trimester) losses.",
            "citation": "Williams Obstetrics, 26th Edition; DC Dutta's Gynaecology"
        },
        {
            "id": "cms2-09",
            "subject": "Preventive & Social Medicine",
            "text": "Under the Indian Public Health Standards (IPHS), a Primary Health Centre (PHC) is established to cater to what population size in plain areas versus hilly/tribal areas?",
            "options": [
                "5,000 (Plain) and 3,000 (Hilly/Tribal)",
                "30,000 (Plain) and 20,000 (Hilly/Tribal)",
                "1,20,000 (Plain) and 80,000 (Hilly/Tribal)",
                "10,000 (Plain) and 5,000 (Hilly/Tribal)"
            ],
            "correct_option": 1,
            "explanation": "IPHS Population Norms: Sub-Centre = 5,000 (Plain) / 3,000 (Hilly/Tribal); Primary Health Centre (PHC) = 30,000 (Plain) / 20,000 (Hilly/Tribal); Community Health Centre (CHC) = 1,20,000 (Plain) / 80,000 (Hilly/Tribal).",
            "citation": "Park's Textbook of Preventive and Social Medicine; IPHS Guidelines MoHFW"
        },
        {
            "id": "cms2-10",
            "subject": "General Surgery",
            "text": "A 45-year-old male with a history of peptic ulcer disease presents with sudden excruciating upper abdominal pain. On physical exam, the abdomen is rigid and 'board-like'. Upright chest X-ray confirms free air (crescent of gas) under the right dome of the diaphragm. What is the diagnosis?",
            "options": [
                "Acute Pancreatitis",
                "Perforated Peptic Ulcer",
                "Strangulated Inguinal Hernia",
                "Acute Mesenteric Ischemia"
            ],
            "correct_option": 1,
            "explanation": "Sudden onset severe generalized abdominal pain with board-like muscular rigidity and pneumoperitoneum (free gas under the diaphragm) is pathognomonic for hollow viscus perforation, most commonly a perforated anterior duodenal or gastric ulcer requiring emergency exploratory laparotomy and Graham's omental patch repair.",
            "citation": "Bailey & Love's Short Practice of Surgery, Chapter on Stomach and Duodenum"
        },
        {
            "id": "cms2-11",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which hormone is responsible for triggering the mid-cycle LH surge that leads directly to ovulation in a normal menstrual cycle?",
            "options": [
                "Progesterone",
                "Sustained peak of 17-beta Estradiol",
                "Inhibin B",
                "Human Chorionic Gonadotropin"
            ],
            "correct_option": 1,
            "explanation": "A critical threshold of Estradiol (>200 pg/mL sustained for at least 48 to 50 hours) secreted by the dominant graafian follicle exerts positive feedback on the pituitary gland and hypothalamus, triggering the massive Luteinizing Hormone (LH) surge that induces ovulation ~34 to 36 hours later.",
            "citation": "DC Dutta's Textbook of Gynaecology; Speroff's Clinical Gynecologic Endocrinology"
        },
        {
            "id": "cms2-12",
            "subject": "Preventive & Social Medicine",
            "text": "Which of the following is considered the single most sensitive indicator of overall community health and socioeconomic development in a country?",
            "options": [
                "Maternal Mortality Ratio (MMR)",
                "Infant Mortality Rate (IMR)",
                "Crude Death Rate (CDR)",
                "Annual Parasite Index (API)"
            ],
            "correct_option": 1,
            "explanation": "Infant Mortality Rate (IMR)—number of infant deaths under 1 year of age per 1,000 live births in a given year—is universally regarded as the most sensitive single index of health, sanitation, nutrition, and general socioeconomic conditions of a population.",
            "citation": "Park's Textbook of Preventive and Social Medicine, Chapter on Demography and Family Planning"
        }
    ],

    "cms-clinical-pharma": [
        {
            "id": "pharma-01",
            "subject": "Clinical Pharmacology",
            "text": "Which of the following is the specific antidote for acute Paracetamol (Acetaminophen) toxicity and what is its primary mechanism of action?",
            "options": [
                "N-Acetylcysteine (NAC); replenishes intracellular glutathione reserves",
                "Flumazenil; competitive antagonism at GABA-A receptors",
                "Deferoxamine; chelates free iron ions",
                "Pralidoxime; reactivates acetylcholinesterase enzyme"
            ],
            "correct_option": 0,
            "explanation": "N-Acetylcysteine (NAC) acts as a glutathione precursor and substitute, binding and detoxifying the hepatotoxic reactive metabolite N-acetyl-p-benzoquinone imine (NAPQI). It is most effective when administered within 8-10 hours of paracetamol ingestion.",
            "citation": "KD Tripathi's Essentials of Medical Pharmacology, 8th Edition; Harrison's Toxicology"
        },
        {
            "id": "pharma-02",
            "subject": "Clinical Pharmacology",
            "text": "A 30-year-old pregnant patient in her third trimester presents with acute pyelonephritis. Which of the following antimicrobial classes is strictly CONTRAINDICATED due to the risk of fetal arthropathy and cartilage damage?",
            "options": [
                "Cephalosporins (e.g. Ceftriaxone)",
                "Fluoroquinolones (e.g. Ciprofloxacin)",
                "Penicillins (e.g. Amoxicillin-Clavulanate)",
                "Macrolides (e.g. Azithromycin)"
            ],
            "correct_option": 1,
            "explanation": "Fluoroquinolones (Ciprofloxacin, Levofloxacin) are contraindicated in pregnancy because they bind to developing connective tissue and cartilage, causing fetal arthropathy and chondrodysplasia in animal studies. Cephalosporins and aminopenicillins are safe in pregnancy.",
            "citation": "KD Tripathi's Essentials of Medical Pharmacology; Briggs Drugs in Pregnancy and Lactation"
        },
        {
            "id": "pharma-03",
            "subject": "Clinical Pharmacology",
            "text": "Which oral anticoagulant acts as a direct Factor Xa inhibitor and does NOT require routine monitoring of PT/INR?",
            "options": [
                "Warfarin",
                "Rivaroxaban",
                "Dabigatran",
                "Unfractionated Heparin"
            ],
            "correct_option": 1,
            "explanation": "Rivaroxaban and Apixaban are Direct Oral Anticoagulants (DOACs) that selectively inhibit Factor Xa directly. Dabigatran, by contrast, is a direct thrombin (Factor IIa) inhibitor. Warfarin requires strict PT/INR monitoring.",
            "citation": "Harrison's Principles of Internal Medicine; KD Tripathi's Pharmacology"
        },
        {
            "id": "pharma-04",
            "subject": "Clinical Pharmacology",
            "text": "Which drug is the treatment of choice for acute anaphylactic shock and what is the recommended adult dose and route?",
            "options": [
                "Epinephrine (Adrenaline) 1:1,000, 0.5 mg Intramuscular in the anterolateral thigh",
                "Epinephrine (Adrenaline) 1:10,000, 1.0 mg rapid IV bolus",
                "Hydrocortisone 100 mg IV alone",
                "Diphenhydramine 50 mg oral"
            ],
            "correct_option": 0,
            "explanation": "Intramuscular Epinephrine (1:1,000 dilution, 0.5 mg in adults, 0.01 mg/kg in children) injected into the vastus lateralis (anterolateral thigh) is the immediate first-line lifesaving drug in anaphylaxis. IV epinephrine bolus without dilution poses severe risk of ventricular fibrillation and cerebral hemorrhage.",
            "citation": "Resuscitation Council UK Anaphylaxis Guidelines; Harrison's Allergy and Clinical Immunology"
        },
        {
            "id": "pharma-05",
            "subject": "Clinical Pharmacology",
            "text": "The classic 'Red Man Syndrome' characterized by flushing, erythema, and pruritus of the face and upper torso is an infusion-related adverse reaction caused by which antibiotic?",
            "options": [
                "Vancomycin",
                "Gentamicin",
                "Clindamycin",
                "Amphotericin B"
            ],
            "correct_option": 0,
            "explanation": "Red Man Syndrome is an adverse reaction caused by rapid intravenous infusion of Vancomycin leading to direct, non-IgE-mediated histamine release from mast cells. It is prevented by slow infusion over at least 60 minutes and pre-treatment with antihistamines.",
            "citation": "KD Tripathi's Essentials of Medical Pharmacology; Goodman & Gilman's Pharmacological Basis of Therapeutics"
        },
        {
            "id": "pharma-06",
            "subject": "Clinical Pharmacology",
            "text": "A patient on chronic Lithium therapy for Bipolar Disorder is started on Hydrochlorothiazide for hypertension. What dangerous drug interaction is likely to occur?",
            "options": [
                "Severe Lithium Toxicity due to decreased renal clearance",
                "Rapid loss of Lithium efficacy due to enhanced excretion",
                "Severe Hyperkalemia",
                "Acute pancreatitis"
            ],
            "correct_option": 0,
            "explanation": "Thiazide diuretics cause sodium depletion at the distal convoluted tubule, which triggers compensatory increased reabsorption of sodium AND lithium in the proximal tubule. This reduces lithium clearance by 25-40% and precipitates severe lithium toxicity (tremors, ataxia, seizures, arrhythmias).",
            "citation": "Harrison's Principles of Internal Medicine; KD Tripathi's Pharmacology"
        }
    ],

    "cms-psm-national-programs": [
        {
            "id": "psm-01",
            "subject": "Preventive & Social Medicine",
            "text": "Under the National Tuberculosis Elimination Program (NTEP) of India, what is the standard first-line intensive phase regimen for drug-sensitive pulmonary tuberculosis in adults?",
            "options": [
                "2 months of daily HRZE (Isoniazid, Rifampicin, Pyrazinamide, Ethambutol)",
                "2 months of thrice-weekly HRZ",
                "6 months of daily Rifampicin alone",
                "3 months of Bedaquiline + Delamanid"
            ],
            "correct_option": 0,
            "explanation": "Under NTEP, the standard treatment regimen for drug-sensitive TB consists of an Intensive Phase of 2 months of daily fixed-dose combinations of 4 drugs: HRZE (Isoniazid, Rifampicin, Pyrazinamide, Ethambutol), followed by a Continuation Phase of 4 months of 3 drugs: HRE (Isoniazid, Rifampicin, Ethambutol).",
            "citation": "NTEP Guidelines, Central TB Division, MoHFW; Park's PSM 26th Edition"
        },
        {
            "id": "psm-02",
            "subject": "Preventive & Social Medicine",
            "text": "Under the Universal Immunization Programme (UIP) of India, which vaccine is administered intradermally at birth or up to 1 year of age over the left deltoid?",
            "options": [
                "BCG (Bacillus Calmette-Guérin)",
                "Hepatitis B birth dose",
                "Oral Polio Vaccine (OPV-0)",
                "Inactivated Polio Vaccine (fIPV)"
            ],
            "correct_option": 0,
            "explanation": "BCG is given intradermally (0.05 mL at birth or 0.1 mL after 1 month up to 1 year) over the left deltoid insertion. A permanent wheal appears, followed in 2-3 weeks by a papule that crusts and forms a typical permanent round scar by 6-12 weeks.",
            "citation": "Universal Immunization Programme Guidelines, MoHFW; Park's PSM"
        },
        {
            "id": "psm-03",
            "subject": "Preventive & Social Medicine",
            "text": "What is the key epidemiological criterion defined by the NVBDCP to confirm that a malaria-endemic area has entered the pre-elimination/elimination phase?",
            "options": [
                "Annual Parasite Index (API) < 1 case per 1,000 population at risk",
                "Slide Positivity Rate (SPR) > 5%",
                "Infant Parasite Rate (IPR) > 10%",
                "Annual Blood Examination Rate (ABER) < 2%"
            ],
            "correct_option": 0,
            "explanation": "The Annual Parasite Index (API = confirmed malaria cases in a year / total population × 1,000) is the primary index to assess malaria transmission. An API < 1 case per 1,000 population indicates that the district has entered the malaria pre-elimination phase.",
            "citation": "NVBDCP National Strategic Plan for Malaria Elimination in India; Park's PSM"
        },
        {
            "id": "psm-04",
            "subject": "Preventive & Social Medicine",
            "text": "According to the Janani Suraksha Yojana (JSY) guidelines, what is the primary objective of the program and how is it implemented?",
            "options": [
                "Promote institutional deliveries among pregnant women via cash incentives to reduce Maternal and Neonatal Mortality",
                "Provide free school meals to adolescent girls",
                "Eradicate iron deficiency in preschool children",
                "Offer compulsory tubectomy incentives"
            ],
            "correct_option": 0,
            "explanation": "Janani Suraksha Yojana (JSY) is a safe motherhood intervention under NHM that integrates cash assistance with antenatal care and institutional delivery in government or accredited private health facilities, directly targeting reductions in MMR and NMR.",
            "citation": "National Health Mission Guidelines; Park's Textbook of Preventive and Social Medicine"
        },
        {
            "id": "psm-05",
            "subject": "Preventive & Social Medicine",
            "text": "Under the Biomedical Waste Management Rules (2016) in India, into which color-coded container must contaminated anatomical waste (placenta, amputated limbs) and soiled bandages be discarded?",
            "options": [
                "Yellow non-chlorinated plastic bag (for Incineration / Deep burial)",
                "Red container (for Autoclaving and recycling)",
                "Blue cardboard box (for Glassware and ampoules)",
                "Translucent white puncture-proof container (for Needles and sharps)"
            ],
            "correct_option": 0,
            "explanation": "BMWM Rules 2016: Yellow bags = Human anatomical waste, animal waste, soiled dressings, expired cytotoxic medicines (treated via incineration or plasma pyrolysis). Red = Contaminated recyclable plastics (catheters, IV tubing). White translucent = Needles, scalpels, sharps. Blue = Glassware and metallic body implants.",
            "citation": "Biomedical Waste Management Rules 2016, Ministry of Environment, Forest and Climate Change; Park's PSM"
        },
        {
            "id": "psm-06",
            "subject": "Preventive & Social Medicine",
            "text": "What is the targeted replacement-level Total Fertility Rate (TFR) required for a population to achieve stabilization?",
            "options": [
                "2.1 children per woman",
                "1.5 children per woman",
                "2.8 children per woman",
                "3.0 children per woman"
            ],
            "correct_option": 0,
            "explanation": "Replacement-level fertility is the average number of children that a couple must bear in their reproductive lifetime to replace themselves. In demography, a Total Fertility Rate (TFR) of 2.1 is defined as replacement level fertility.",
            "citation": "NFHS-5 Report; Park's Textbook of Preventive and Social Medicine, Demography chapter"
        }
    ],

    "esic-imo-clinical-drill": [
        {
            "id": "esic-01",
            "subject": "Emergency Medicine",
            "text": "An agricultural industrial worker is brought to casualty with excessive salivation, pinpoint pupils (miosis), bilateral diffuse rhonchi, bradycardia, and fasciculations following pesticide exposure. What is the immediate pharmacological antidote of choice?",
            "options": [
                "Atropine Sulfate IV until signs of full atropinization (clearing of bronchorrhea) appear",
                "Physostigmine IV",
                "Naloxone IV",
                "Sodium Thiosulfate IV"
            ],
            "correct_option": 0,
            "explanation": "The clinical picture of SLUDGE (Salivation, Lacrimation, Urination, Defecation, GI cramps, Emesis) with miosis and bronchorrhea confirms acute Organophosphate Poisoning. Intravenous Atropine (1.8-3 mg bolus, doubled every 5 minutes until pulmonary secretions clear and heart rate >80 bpm) is the immediate lifesaving muscarinic antagonist.",
            "citation": "Harrison's Principles of Internal Medicine; KD Tripathi's Medical Pharmacology"
        },
        {
            "id": "esic-02",
            "subject": "General Medicine",
            "text": "A 52-year-old factory supervisor presents to the dispensary with crushing retrosternal chest pain of 45 minutes duration. 12-lead ECG reveals 3 mm ST-segment elevation in leads V1 to V4. What is the immediate antiplatelet loading dose protocol recommended prior to emergency referral for PCI or thrombolysis?",
            "options": [
                "Aspirin 325 mg chewed + Clopidogrel 300-600 mg oral load",
                "Low molecular weight heparin alone",
                "Aspirin 75 mg daily starting next morning",
                "Streptokinase 1.5 million units oral"
            ],
            "correct_option": 0,
            "explanation": "In acute ST-Elevation Myocardial Infarction (STEMI), Dual Antiplatelet Therapy (DAPT) with chewed non-enteric coated Aspirin (162-325 mg) plus a P2Y12 inhibitor (Clopidogrel 300-600 mg or Ticagrelor 180 mg) should be administered immediately upon diagnosis unless contraindicated.",
            "citation": "AHA/ACC STEMI Management Guidelines; Harrison's Cardiology"
        },
        {
            "id": "esic-03",
            "subject": "Preventive & Social Medicine",
            "text": "A patient presents with a deep transdermal dog bite on the right calf with active oozing of blood (WHO Category III exposure). What is the mandatory immediate post-exposure prophylaxis protocol?",
            "options": [
                "Immediate wound washing under running tap water with soap for 15 minutes, local infiltration of Rabies Immunoglobulin (RIG), and Modern Cell Culture Vaccine (IM on Days 0, 3, 7, 28)",
                "Anti-rabies vaccine alone on Day 0 and Day 3",
                "Primary suturing of the wound immediately under local anesthesia",
                "Tetanus toxoid only with observation of dog for 10 days"
            ],
            "correct_option": 0,
            "explanation": "WHO Category III animal bites (transdermal bites or scratches, licks on broken skin) strictly require: 1) Vigorous washing with soap and water for at least 15 minutes; 2) Rabies Immunoglobulin (HRIG 20 IU/kg) infiltrated directly into and around the wound; 3) Rabies vaccination on days 0, 3, 7, and 28. Wounds should NOT be primarily sutured.",
            "citation": "National Guidelines on Rabies Prophylaxis, NVBDCP / MoHFW; Park's PSM"
        },
        {
            "id": "esic-04",
            "subject": "Emergency Medicine",
            "text": "A 30-year-old patient is brought to casualty in continuous generalized tonic-clonic status epilepticus lasting >10 minutes. What is the first-line intravenous benzodiazepine of choice?",
            "options": [
                "IV Lorazepam (0.1 mg/kg given at 2 mg/min)",
                "IV Phenytoin 15 mg/kg bolus",
                "Oral Carbamazepine",
                "IV Propofol infusion"
            ],
            "correct_option": 0,
            "explanation": "Intravenous Lorazepam (0.1 mg/kg up to 4 mg bolus) is the universally preferred first-line agent for terminating early status epilepticus due to its rapid onset and longer duration of action in brain tissue compared to Diazepam.",
            "citation": "Neurocritical Care Society Guidelines for Status Epilepticus; Harrison's Neurology"
        },
        {
            "id": "esic-05",
            "subject": "General Medicine",
            "text": "Which chest X-ray finding is characteristically associated with Silicosis in stone-crushing and pottery industrial workers under the ESI Act?",
            "options": [
                "'Eggshell calcification' of hilar lymph nodes and multiple nodular opacities in upper lung zones",
                "Pleural plaques in lower lung zones with asbestosis",
                "Cavitation in bilateral apices with air-fluid levels",
                "Honeycombing with basal subpleural reticulation"
            ],
            "correct_option": 0,
            "explanation": "Eggshell calcification (peripheral rim calcification of enlarged hilar and mediastinal lymph nodes) along with diffuse rounded nodular opacities predominantly affecting the upper lung zones is pathognomonic for chronic Silicosis.",
            "citation": "Park's Textbook of Preventive and Social Medicine, Chapter on Occupational Health; Harrison's Pulmonology"
        },
        {
            "id": "esic-06",
            "subject": "Emergency Medicine",
            "text": "A rural laborer presents 2 hours after a Russel's Viper bite with severe local swelling, bleeding from gums, and prolonged Whole Blood Clotting Time (20WBCT > 20 minutes). How many vials of Polyvalent Anti-Snake Venom (ASV) are initially indicated?",
            "options": [
                "10 vials of reconstituted Polyvalent ASV infused in 0.9% Normal Saline over 1 hour",
                "1 vial administered subcutaneously",
                "2 vials administered intramuscularly",
                "50 vials given as rapid IV push"
            ],
            "correct_option": 0,
            "explanation": "According to the National Snakebite Management Protocol of India, in patients with systemic envenomation (hemotoxicity or neurotoxicity), the initial dose is 10 vials of Lyophilized Polyvalent Anti-Snake Venom (ASV) reconstituted in 500 mL of normal saline and infused intravenously over 1 hour.",
            "citation": "National Protocol for Management of Snakebites, MoHFW India"
        }
    ],

    "upsc-cms-2026-paper-1-authentic": [
        {
            "id": "cms26-p1-001",
            "subject": "General Medicine",
            "text": "A 35-year-old man presented with serial blood 4. pressure recordings of above 140/90 mmHg. Which one of the following signs is not a clue for an underlying cause of hypertension (secondary hypertension) ?",
            "options": [
                "Radio-femoral delay",
                "Enlarged kidneys",
                "Bull neck and buffalo hump",
                "Vitiligo"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Vitiligo.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.1)"
        },
        {
            "id": "cms26-p1-002",
            "subject": "General Medicine",
            "text": "A 71-year-old male presents with headache, dizziness, nausea with palpitations. The patient is already on treatment for diabetes and hypertension. The blood pressure reading is 220/140 mmHg. Which of the following statements is/are correct? 1. This is a case of hypertensive emergency which can be managed by intravenous sodium nitroprusside. 2. An immediate normalization of the blood pressure should be the target. 3. Secondary causes of hypertension like renovascular disease are uncommon in patients with hypertensive emergency. Select the answer using the code given below :",
            "options": [
                "1 only",
                "1, 2 and 3",
                "2 and 3 only",
                "1 and 3 only"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.2)"
        },
        {
            "id": "cms26-p1-003",
            "subject": "General Medicine",
            "text": "Match List I with List II and select the correct answer using the code given below the lists: List I List Il (Drug used in heart (Mechanism of failure) action) A. Metoprolol 1. Aldosterone antagonist B. Telmisartan 2. Angiotensin- receptor blocker C. Enalapril 3. ACE inhibitor D. Eplerenone 4. Beta-blocker Code : B C D",
            "options": [
                "4 2",
                "4 2 1",
                "2 4",
                "1 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 4 2 1.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.3)"
        },
        {
            "id": "cms26-p1-004",
            "subject": "General Medicine",
            "text": "Consider the following statements regarding Takotsubo cardiomyopathy : 1. There is acute right ventricular dysfunction characterized by dilatation of the right ventricular apex. 2. It can be precipitated by acute emotional stress and is frequently associated with an underlying neuro-psychiatric disorder. 3. Symptoms and ECG findings often mimic acute ST-elevation myocardial infarction. 4. Ventriculography shows normal left ventricle and apical ballooning of the right ventricle. Which of the statements given above are correct?",
            "options": [
                "1 and 2",
                "2 and 3",
                "1 and 4",
                "3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.4)"
        },
        {
            "id": "cms26-p1-005",
            "subject": "General Medicine",
            "text": "With regard to Hypertrophic Cardiomyopathy, match List I with List II and select the correct answer using the code given below the lists : List I List II (Mutation) (Phenotype) A. Beta-myosin heavy 1. Marked chain mutations ventricular hypertrophy B. Troponin 2. Hypertension mutations and arrhythmia C. Myosin-binding 3. Myocardial fibre protein-C mutations disarray with minimal hypertrophy Code : B C",
            "options": [
                "1 2",
                "1 2",
                "2 1",
                "2"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1 2.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.5)"
        },
        {
            "id": "cms26-p1-006",
            "subject": "General Medicine",
            "text": "iTumour Plop' is a characteristic auscultatory finding seen in which one of the following conditions?",
            "options": [
                "Atrial myxoma",
                "Arrhythmogenic ventricular cardiomyopathy",
                "Constrictive pericarditis",
                "Dilated cardiomyopathy Retinal ischaemia, flame-shaped"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Atrial myxoma.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.6)"
        },
        {
            "id": "cms26-p1-007",
            "subject": "General Medicine",
            "text": "haemorrhages and cotton-wool exudates are fundoscopy findings in which of the following grades of hypertensive retinopathy? 1. Grade 1 2. Grade 2 3. Grade 3 4. Grade 4 Select the correct answer using the code given below :",
            "options": [
                "1 and 2 only",
                "3 and 4 only",
                "2, 3 and 4 only",
                "1, 2, 3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 3 and 4 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.7)"
        },
        {
            "id": "cms26-p1-008",
            "subject": "General Medicine",
            "text": "Aschoff Nodules are a pathognomonic cardiac finding in which one of the following conditions?",
            "options": [
                "Rheumatic carditis",
                "Infective endocarditis",
                "Rheumatoid arthritis",
                "Takayasu's arteritis"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Rheumatic carditis.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.8)"
        },
        {
            "id": "cms26-p1-009",
            "subject": "General Medicine",
            "text": "Consider the following statements regarding Eisenmenger Syndrome : 1. In patients with severe and prolonged pulmonary hypertension, the right-to-left shunt gets reversed to a left-to-right shunt. 2. There is marked cyanosis, which may be more apparent in the feet and toes than in the upper part of the body. 3. Antihypertensives which cause peripheral vasodilatation can exacerbate the shunting and worsen the symptoms. Which of the statements given above is/are correct?",
            "options": [
                "1 only",
                "2 only",
                "1 and 3",
                "2 and 3"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.9)"
        },
        {
            "id": "cms26-p1-010",
            "subject": "General Medicine",
            "text": "Consider the following statements regarding the murmur of Patent Ductus Arteriosus : 1. It is a continuous 'machinery' murmur. 2. There is a late diastolic accentuation. 3. It is maximal in the second left intercostal space below the clavicle. 4. With the development of Eisenmenger Syndrome, the murmur becomes louder and rumbling in character. Which of the statements given above is/are correct?",
            "options": [
                "1 only",
                "1 and 3",
                "2 and 3 only",
                "2, 3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1 and 3.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.10)"
        },
        {
            "id": "cms26-p1-011",
            "subject": "General Medicine",
            "text": "of the chest. On examination, there was dullness on percussion on left infra-axillary area. X-ray Chest showed left opaque hemithorax. Which one of the following is an indication for tube thoracentesis in this case ?",
            "options": [
                "Presence of straw-coloured fluid",
                "Pleural fluid pH > 7-2",
                "Pleural fluid glucose < 60 mg/dL",
                "Pleural fluid LDH < 600 IU/L"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Pleural fluid glucose < 60 mg/dL.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.11)"
        },
        {
            "id": "cms26-p1-012",
            "subject": "General Medicine",
            "text": "A patient with a history of smoking presents to the emergency with a complaint of breathlessness for the last two days. On examination, he was found to be cyanosed and had bilateral rhonchi. ABG was done, which shows : pH 7•12 PaCO2 : 80 mmHg PaOz 46 mmHg HCO- : 29 mEq/L Based on the history, clinical examination and ABG finding, the most likely diagnosis is :",
            "options": [
                "Pulmonary embolism",
                "Pneumonia",
                "COPD exacerbation",
                "Pulmonary fibrosis"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — COPD exacerbation.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.12)"
        },
        {
            "id": "cms26-p1-013",
            "subject": "General Medicine",
            "text": "A patient presented with pain on the left side 13. A patient with a history of chronic smoking presented with breathlessness for the last one year. On examination, there were bilateral rhonchi in the chest. The Chest X-ray was suggestive of hyper-inflated lung field. Which of the following parameters of the pulmonary function test are consistent with the diagnosis of chronic obstructive pulmonary disease in this case ? 1. Decreased FEV1 2. Increased diffusion capacity 3. Increased residual volume 4. Decreased peak expiratory flow rate Select the correct answer using the code given below :",
            "options": [
                "1, 2 and 3",
                "1, 3 and 4",
                "2, 3 and 4",
                "2 and 4 only"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.13)"
        },
        {
            "id": "cms26-p1-014",
            "subject": "General Medicine",
            "text": "Omalizumab is helpful in which of the following diseases ? Asthma Idiopathic pulmonary fibrosis Nasal polyposis Select the correct answer using the code given below :",
            "options": [
                "1 and 3 only",
                "1 and 2 only",
                "1, 2 and 3",
                "2 and 3 only"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1 and 3 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.14)"
        },
        {
            "id": "cms26-p1-015",
            "subject": "General Medicine",
            "text": "A 50-year-old male working in a stone industry presents with breathlessness and cough. CT Chest shows calcified mediastinal lymph nodes and pulmonary nodules. He is diagnosed with silicosis. Which of the following statements are correct? 1. Silicosis typically involves lower lobes of the lung. 2. The patient is at a higher risk of developing pulmonary tuberculosis. 3. Pulmonary fibrosis after occupational exposure to silica is dose-dependent. Select the correct answer using the code given below :",
            "options": [
                "1 and 2 only",
                "1, 2 and 3",
                "1 and 3 only",
                "2 and 3 only"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 2 and 3 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.15)"
        },
        {
            "id": "cms26-p1-016",
            "subject": "General Medicine",
            "text": "A 70-year-old male, with a history of smoking presents with progressive dyspnea and dry cough. Examination reveals clubbing and fine basal crackles. Spirometry shows low forced vital capacity (FVC) and low diffusion capacity (DLCO). CT Chest shows extensive bilateral reticular shadows and subpleural honeycombing. What is the most likely diagnosis ?",
            "options": [
                "Idiopathic pulmonary fibrosis",
                "Sarcoidosis",
                "Chronic obstructive pulmonary disease",
                "Bronchiectasis"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Idiopathic pulmonary fibrosis.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.16)"
        },
        {
            "id": "cms26-p1-017",
            "subject": "General Medicine",
            "text": "A 40-year-old obese bank accountant presents with complaints of excessive daytime sleepiness and fatigue. His spouse reports that he has loud snoring and early morning tiredness. Which of the following statements is/are correct? 1. The patient is most likely suffering from obstructive sleep apnea. 2. The diagnosis requires CT/MRI of the neck. 3. Treatment of choice is Zolpidem. Select the correct answer using the code given below :",
            "options": [
                "1 only",
                "2 only",
                "2 and 3",
                "1 and 3"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.17)"
        },
        {
            "id": "cms26-p1-018",
            "subject": "General Medicine",
            "text": "A 34-year-old medical student has fever, chest pain, severe breathlessness, and dry cough. Chest X-ray shows right homogeneous opacity. Ultrasound lung confirms massive pleural effusion on the right side. Which of the following statements are correct? 1. A therapeutic pleural tap should be done to relieve dyspnoea and sent for analysis. 2. If pleural fluid analysis is inconclusive, a thoracoscopy may be done. 3. Thoracoscopy should be done under general anesthesia. Select the correct answer using the code given below :",
            "options": [
                "1 and 2 only",
                "2 and 3 only",
                "1 and 3 only",
                "1, 2 and 3"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1 and 2 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.18)"
        },
        {
            "id": "cms26-p1-019",
            "subject": "General Medicine",
            "text": "A 42-year-old male with chronic kidney disease undergoing chronic dialysis presents with worsening breathlessness. Examination reveals muffled heart. sounds. Chest X-ray image is shown below. What is the most likely diagnosis of this patient?",
            "options": [
                "Pneumothorax",
                "Pleural effusion",
                "Pericardial effusion",
                "Pulmonary embolism"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Pericardial effusion.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.19)"
        },
        {
            "id": "cms26-p1-020",
            "subject": "General Medicine",
            "text": "A 22-year-old male presents with left-sided chest pain and breathlessness after a road traffic accident. Examination reveals absent left-sided breath sounds. CT Chest image is shown below. What is the diagnosis of this patient ?",
            "options": [
                "Pneumothorax",
                "Pleural effusion",
                "Lung cavity",
                "Bowel loops herniation"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Bowel loops herniation.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.20)"
        },
        {
            "id": "cms26-p1-021",
            "subject": "General Medicine",
            "text": "Infiltration of the small-intestine mucosa with 'foamy' macrophages, which stain positive with Periodic Acid-Schiff (PAS) reagent, is a characteristic feature of which one of the following conditions?",
            "options": [
                "Radiation enteropathy",
                "Coeliac disease",
                "Tropical sprue",
                "Whipple's disease"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Whipple's disease.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.21)"
        },
        {
            "id": "cms26-p1-022",
            "subject": "General Medicine",
            "text": "Which one of the following is not a risk factor for the acquisition of chronic hepatitis C?",
            "options": [
                "Intravenous drug abuse",
                "Unscreened infected blood transfusion",
                "Vertical transmission",
                "Sharing food"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Sharing food.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.22)"
        },
        {
            "id": "cms26-p1-023",
            "subject": "General Medicine",
            "text": "Which one of the following is a predictor of liver fibrosis ?",
            "options": [
                "Serum transaminase levels",
                "AST-to-Platelet Ratio Index",
                "Coagulation profile",
                "Serum albumin and pre-albumin"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — AST-to-Platelet Ratio Index.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.23)"
        },
        {
            "id": "cms26-p1-024",
            "subject": "General Medicine",
            "text": "A 30-year-old female with irritable bowel syndrome presents with predominant symptom of diarrhea. Which of the following will be helpful in her treatment? 1. Loperamide 2. Lactulose 3. Lubiprostone 4. Sorbitol Select the correct answer using the code given below :",
            "options": [
                "1 and 2",
                "1 only",
                "2 and 3",
                "2 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.24)"
        },
        {
            "id": "cms26-p1-025",
            "subject": "General Medicine",
            "text": "'Melanosis coli' (brownish discoloration of colonic mucosa) can occur due to the long-term consumption of which one of the following ?",
            "options": [
                "Stimulant laxatives",
                "Non-steroidal anti-inflammatory drugs",
                "Proton pump inhibitors",
                "generation cephalosporins"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Stimulant laxatives.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.25)"
        },
        {
            "id": "cms26-p1-026",
            "subject": "General Medicine",
            "text": "Patients suffering from which of the following condition(s) can get symptomatic relief by consuming a gluten-free diet? 1. Coeliac disease 2. Peptic ulcer disease 3. Dermatitis herpetiformis Select the correct answer using the code given below :",
            "options": [
                "1 only",
                "1 and 3 only",
                "2 and 3 only",
                "1, 2 and 3"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1 and 3 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.26)"
        },
        {
            "id": "cms26-p1-027",
            "subject": "General Medicine",
            "text": "The '13C-urea breath test' and the 'faecal antigen test' are non-invasive techniques to diagnose infection with which one of the following ?",
            "options": [
                "Haemophilus inftuenzae",
                "Leishmania donovani",
                "Giardia lamblia",
                "Helicobacter pylori"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Helicobacter pylori.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.27)"
        },
        {
            "id": "cms26-p1-028",
            "subject": "General Medicine",
            "text": "Consider the following statements regarding Ménétrier's disease : 1. There is excessive production of Transforming Growth Factor-alpha (TGF-a). 2. Majority of the patients present with features of protein-losing enteropathy. 3. Mucus secreting cells are replaced by parietal and chief cells. 4. The mucosal folds of the body and fundus of the stomach are greatly enlarged. Which of the statements given above are correct?",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1, 2 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.28)"
        },
        {
            "id": "cms26-p1-029",
            "subject": "General Medicine",
            "text": "Consider the following statements regarding 'Barrett's Oesophagus' : 1. It is a pre-malignant condition. 2. The normal columnar mucosa of lower oesophagus is replaced by squamous cells. 3. It is an adaptive response to chronic gastro-oesophageal reflux. Which of the statements given above is/are correct?",
            "options": [
                "3 only",
                "1 and 2 only",
                "1 and 3 only",
                "1, 2 and 3"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 1 and 3 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.29)"
        },
        {
            "id": "cms26-p1-030",
            "subject": "General Medicine",
            "text": "The presence of which of the following is suggestive of metastatic spread of an underlying gastrointestinal malignancy ? Krukenberg Tumour Virchow's Node Meigs' Syndrome 4. Sister Mary Joseph's Nodule Select the correct answer using the code given below :",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1, 2 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.30)"
        },
        {
            "id": "cms26-p1-031",
            "subject": "General Medicine",
            "text": "Sodium zirconium cyclosilicate and patiromer are commonly prescribed to chronic kidney disease patients because of their property of binding to which one of the following electrolytes ?",
            "options": [
                "Calcium",
                "Sodium",
                "Potassium",
                "Phosphate"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Potassium.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.31)"
        },
        {
            "id": "cms26-p1-032",
            "subject": "General Medicine",
            "text": "Calcium resonium, which is used to treat hyperkalaemia over a short-term in chronic kidney disease, is associated with the development of which one of the following conditions ?",
            "options": [
                "Prostatomegaly",
                "Myocarditis",
                "Renal Artery Stenosis",
                "Bowel Necrosis"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Bowel Necrosis.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.32)"
        },
        {
            "id": "cms26-p1-033",
            "subject": "General Medicine",
            "text": "In multiple monoclonal immunoglobulin light chains combine with Tamm - Horsfall protein precipitate in the renal tubules which leads to the development of which one of the following conditions?",
            "options": [
                "IgA Nephropathy",
                "Cast Nephropathy",
                "Membranous Glomerulonephritis",
                "Interstitial Nephritis"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Cast Nephropathy.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.33)"
        },
        {
            "id": "cms26-p1-034",
            "subject": "General Medicine",
            "text": "Multiple myeloma can cause proximal tubular injury due to light chain deposition in the tubular epithelium causing acquired Fanconi Syndrome. Which of the following are characteristic findings in this condition? Little/no proteinuria 2. Aminoaciduria 3. Phosphaturia 4. Glycosuria Select the correct answer using the code given below :",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 2, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.34)"
        },
        {
            "id": "cms26-p1-035",
            "subject": "General Medicine",
            "text": "Which one of the following hereditary tubulo-interstitial kidney diseases shows Autosomal Recessive pattern of inheritance?",
            "options": [
                "Nephronophthisis",
                "Juvenile hyperuricaemic nephropathy",
                "Medullary cystic kidney disease type 1",
                "Medullary cystic kidney disease type 2"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Nephronophthisis.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.35)"
        },
        {
            "id": "cms26-p1-036",
            "subject": "General Medicine",
            "text": "Which one of the following is a contraindication of Renal Biopsy ?",
            "options": [
                "Nephritic syndrome",
                "Acute renal injury of uncertain etiology",
                "Uncontrolled hypertension",
                "Renal transplant dysfunction"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Uncontrolled hypertension.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.36)"
        },
        {
            "id": "cms26-p1-037",
            "subject": "General Medicine",
            "text": "Anti-PLA2R antibodies, which are directed against the M-type phospholipase A2 receptor', are a key biomarker for which one of the following conditions?",
            "options": [
                "Primary membranous nephropathy",
                "IgA Nephropathy",
                "Crescentic glomerulonephritis",
                "Mesangioproliferative glomerulonephritis"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Primary membranous nephropathy.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.37)"
        },
        {
            "id": "cms26-p1-038",
            "subject": "General Medicine",
            "text": "Which one of the following stages of chronic kidney disease corresponds to a glomerular filtration rate of 55 mL/min/1•73 m2 ?",
            "options": [
                "1",
                "2",
                "ЗА",
                "3B"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — ЗА.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.38)"
        },
        {
            "id": "cms26-p1-039",
            "subject": "General Medicine",
            "text": "Which one of the following hereditary neuropathies is characterized by elevated serum 'phytanic acid' levels and manifests with the tetrad of peripheral neuropathy, retinitis pigmentosa, cerebellar ataxia and elevated protein concentration in cerebrospinal fluid?",
            "options": [
                "Krabbe's disease",
                "Fabry's disease",
                "Tangier disease",
                "Refsum's disease"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Refsum's disease.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.39)"
        },
        {
            "id": "cms26-p1-040",
            "subject": "General Medicine",
            "text": "Which one of the following is true regarding asymmetrical motor diabetic neuropathy?",
            "options": [
                "Weakness and wasting of proximal muscles of lower limbs",
                "Painless wasting of muscles",
                "Hyper-exaggerated reflexes in the affected limb",
                "Glucocorticoids are the treatment of choice"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Weakness and wasting of proximal muscles of lower limbs.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.40)"
        },
        {
            "id": "cms26-p1-041",
            "subject": "General Medicine",
            "text": "Which of the following are the clinical features of multiple sclerosis ? 1. Loss or blurring of vision 2. Tingling in limbs on neck flexion 3. Generalized tonic-clonic seizures 4. Gait ataxia Select the correct answer using the code given below :",
            "options": [
                "1, 2 and 4",
                "2, 3 and 4",
                "2 and 4 only",
                "1 and 3"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1, 2 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.41)"
        },
        {
            "id": "cms26-p1-042",
            "subject": "General Medicine",
            "text": "A 42-year-old labourer developed a sudden, severe and persistent headache, accompanied by vomiting and neck pain. He was evaluated at the nearest hospital where an emergency computed tomography was negative for stroke. Which one of the following investigations is best to confirm the diagnosis ?",
            "options": [
                "Electroencephalogram",
                "Carotid Doppler",
                "Lumbar puncture after 12 hours",
                "Upper gastrointestinal endoscopy"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Lumbar puncture after 12 hours.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.42)"
        },
        {
            "id": "cms26-p1-043",
            "subject": "General Medicine",
            "text": "Consider the following pairs with respect to muscle channelopathies : (Channel) (Muscle disease) 1. Sodium - Paramyotonia congenita 2. Calcium - Malignant hyperthermia 3. Ryanodine receptor - Becker disease 4. Chloride - Thomsen disease Which of the pairs given above are correctly matched ?",
            "options": [
                "1, 2, 3 and 4",
                "1, 3 and 4 only",
                "1, 2 and 4 only",
                "2 and 3 only"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 1, 2 and 4 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.43)"
        },
        {
            "id": "cms26-p1-044",
            "subject": "General Medicine",
            "text": "A 47-year-old man with a large frontoparietal lesion in the right hemisphere was asked to circle all the A's. Only targets on the right were circled. This is a manifestation of :",
            "options": [
                "Left hemispatial neglect",
                "Simultanagnosia",
                "Constructional apraxia",
                "Alien hand syndrome"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Left hemispatial neglect.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.44)"
        },
        {
            "id": "cms26-p1-045",
            "subject": "General Medicine",
            "text": "A 40-year-old man was found to have weakness of the right shoulder and arm 48. 6 hours before presentation. This was followed by weakness of the ipsilateral leg, then left leg, followed by left arm (around-the-clock pattern). Where in the neuraxis is the lesion likely to be present?",
            "options": [
                "Cerebral cortex",
                "Foramen magnum",
                "Midbrain",
                "Pons"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Foramen magnum.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.45)"
        },
        {
            "id": "cms26-p1-046",
            "subject": "General Medicine",
            "text": "Which one of the following refers to agraphesthesia?",
            "options": [
                "Inability to identify common objects by palpation recognising their shape, texture and size",
                "Inability to recognize with eyes closed, letters or numbers drawn by the examiner's fingertip on the palm of the hand",
                "Inability to discriminate two points set 3 mm apart on fingertips",
                "Inability to stand and walk with both the eyes closed"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Inability to recognize with eyes closed, letters or numbers drawn by the examiner's fingertip on the palm of the hand.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.46)"
        },
        {
            "id": "cms26-p1-047",
            "subject": "General Medicine",
            "text": "Which one of the following is a type of Mitochondrial myopathy ?",
            "options": [
                "Myoclonic epilepsy with ragged red fibres",
                "Familial focal epilepsy with variable foci",
                "Sleep related hypermotor epilepsy",
                "Severe myoclonic epilepsy of infancy"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Myoclonic epilepsy with ragged red fibres.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.47)"
        },
        {
            "id": "cms26-p1-048",
            "subject": "General Medicine",
            "text": "Which one of the following is a childhood onset epilepsy syndrome characterized by multiple seizure types, developmental delay and slow (< 3 Hz) spike-and-wave discharges on an electroencephalogram ?",
            "options": [
                "Juvenile Myoclonic Epilepsy Syndrome",
                "Lennox-Gastaut Syndrome",
                "Mesial Temporal Lobe Epilepsy Syndrome",
                "Rasmussen Syndrome"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Lennox-Gastaut Syndrome.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.48)"
        },
        {
            "id": "cms26-p1-049",
            "subject": "General Medicine",
            "text": "With regard to the treatment of 51. phaeochromocytoma, beta-blocker should never be given before alpha-blocker because it may cause :",
            "options": [
                "Paradoxical rise in blood pressure due to unopposed alpha-mediated vasoconstriction",
                "Paradoxical fall in blood pressure due to unopposed alpha-mediated vasoconstriction",
                "Paradoxical rise in blood pressure due to unopposed alpha-mediated vasodilatation",
                "Paradoxical fall in blood pressure due to unopposed alpha-mediated vasodilatation"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Paradoxical rise in blood pressure due to unopposed alpha-mediated vasoconstriction.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.49)"
        },
        {
            "id": "cms26-p1-050",
            "subject": "General Medicine",
            "text": "Which of the following may be seen during clinical examination in a patient of Diabetes mellitus ? 1. Necrobiosis lipoidica 2. Charcot neuroarthropathy 3. Exudative maculopathy 4. Acanthosis nigricans Select the correct answer using the code given below :",
            "options": [
                "1 only",
                "1 and 2 only",
                "2 and 3 only",
                "1, 2, 3 and 4"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 1, 2, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.50)"
        },
        {
            "id": "cms26-p1-051",
            "subject": "General Medicine",
            "text": "Consider the following statements regarding glucagon-like peptide-1 (GLP-1) and gastric inhibitory polypeptide (GIP) : 1. GLP-1 is an incretin hormone. 2. GIP is an incretin hormone. 3. GLP-1 is released from gastrointestinal 'L-cells'. 4. GIP is released from gastrointestinal 'M-cells'. Which of the statements given above are correct?",
            "options": [
                "1 and 2 only",
                "1, 2 and 3",
                "3 and 4 only",
                "2, 3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1, 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.51)"
        },
        {
            "id": "cms26-p1-052",
            "subject": "General Medicine",
            "text": "Consider the following statements regarding 'Factitious Thyrotoxicosis' : 1. Induced when patients consume excessive amounts of levothyroxine. 2. The exogenous levothyroxine supresses secretion of pituitary TSH (thyroid-stimulating hormone). 3. Serum thyroglobulin level is elevated. 4. T4 : T3 ratio is high. Which of the statements given above are correct?",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1, 2 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.52)"
        },
        {
            "id": "cms26-p1-053",
            "subject": "General Medicine",
            "text": "Deficiency of which of the following mineral(s) can lead to hypocalcemia by impairing the ability of the parathyroid gland to secrete parathyroid hormone? 1. Phosphate 2. Magnesium 3. Sodium 4. Potassium Select the correct answer using the code given below :",
            "options": [
                "1 and 2",
                "2 only",
                "3 and 4",
                "3 only"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 2 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.53)"
        },
        {
            "id": "cms26-p1-054",
            "subject": "General Medicine",
            "text": "Which of the following are long-acting insulin analogues ? 1. Lispro 2. Glargine 3. Detemir Degludec Select the correct answer using the code given below :",
            "options": [
                "2 only",
                "2 and 4",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 2, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.54)"
        },
        {
            "id": "cms26-p1-055",
            "subject": "General Medicine",
            "text": "Which one of the following levels of hypoglycaemia corresponds to a blood glucose level of 50 mg/dL leading to cognitive impairment and need for corrective treatment?",
            "options": [
                "Level 0",
                "Level 1",
                "Level 2",
                "Level 3"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Level 3.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.55)"
        },
        {
            "id": "cms26-p1-056",
            "subject": "General Medicine",
            "text": "Liquorice misuse, by inhibiting 11 beta-hydroxysteroid dehydrogenase type 2 enzyme, can cause a condition which resembles the clinical features of :",
            "options": [
                "Gonadotropin excess",
                "Thyrotropin excess",
                "Mineralocorticoid excess",
                "Parathyroid hormone excess"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Mineralocorticoid excess.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.56)"
        },
        {
            "id": "cms26-p1-057",
            "subject": "General Medicine",
            "text": "Which of the following is/are growth hormone receptor antagonist(s) indicated in the treatment of Acromegaly ? 1. Octreotide 2. Lanreotide Pasireotide 4. Pegvisomant Select the correct answer using the code given below :",
            "options": [
                "1 and 2 only",
                "3 and 4",
                "1, 2 and 3",
                "4 only"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 4 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.57)"
        },
        {
            "id": "cms26-p1-058",
            "subject": "General Medicine",
            "text": "Which of the following statements regarding Autoimmune Polyendocrine Syndromes (APS) is/are correct? 1. APS Type 1 is more common than APS Type 2. 2. APS Type 1 is inherited as an autosomal recessive condition. 3. APS Type 2 is inherited as an autosomal dominant condition. Select the correct answer using the code given below :",
            "options": [
                "1 only",
                "1 and 2 only",
                "2 and 3 only",
                "1, 2 and 3"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 2 and 3 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.58)"
        },
        {
            "id": "cms26-p1-059",
            "subject": "General Medicine",
            "text": "Which one of the following drugs is not a secondary cause of weight gain?",
            "options": [
                "Sulphonylureas",
                "Glucocorticoids",
                "Thyroxine",
                "B-blockers"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Thyroxine.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.59)"
        },
        {
            "id": "cms26-p1-060",
            "subject": "General Medicine",
            "text": "Which one of the following is true for Teriparatide for treatment of osteoporosis ?",
            "options": [
                "It inhibits bone resorption by neutralizing effect of RANKL.",
                "It is a fragment of human PTH and works by stimulating new bone formation.",
                "It is administered subcutaneously once a year for 5 years.",
                "Teriparatide should be combined with"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — It is a fragment of human PTH and works by stimulating new bone formation..",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.60)"
        },
        {
            "id": "cms26-p1-061",
            "subject": "General Medicine",
            "text": "bisphosphonates for better efficacy. 61. Post-transplant lymphoproliferative disorder, a lymphoma that follows organ transplantation, is associated with infection with which one of the following ?",
            "options": [
                "Epstein-Barr virus",
                "Mycobacterium tuberculosis",
                "Capnocytophaga canimorsus",
                "Histoplasma capsulatum"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Epstein-Barr virus.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.61)"
        },
        {
            "id": "cms26-p1-062",
            "subject": "General Medicine",
            "text": "'Exanthem Subitum' is caused due to infection of which of the following viruses? 1. Human herpesvirus 6 2. Hepatitis-B virus 3. Human herpesvirus 7 4. Hepatitis-C virus Select the correct answer using the code given below :",
            "options": [
                "2 and 4",
                "1 and 2",
                "1 and 3",
                "3 and 4"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 1 and 3.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.62)"
        },
        {
            "id": "cms26-p1-063",
            "subject": "General Medicine",
            "text": "'Slapped-cheek' rash is caused by infection with which one of the following viruses?",
            "options": [
                "Zika virus",
                "Human herpesvirus 6",
                "Parvovirus B-19",
                "Varicella zoster virus"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Parvovirus B-19.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.63)"
        },
        {
            "id": "cms26-p1-064",
            "subject": "General Medicine",
            "text": "The neuropsychiatric manifestations of the 68. A 35-year-old female infections caused by which one of the following infectious agents presents as Muttering Delirium' or 'Coma Vigil' in which patients pick randomly at bed clothes or imaginary objects ?",
            "options": [
                "Neisseria gonorrheae",
                "Cardiobacterium hominis",
                "Salmonella typhi",
                "Campylobacter jejuni"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Salmonella typhi.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.64)"
        },
        {
            "id": "cms26-p1-065",
            "subject": "General Medicine",
            "text": "Necrotizing fasciitis caused by fungi such as mucoraceous moulds is classified as which one of the following types?",
            "options": [
                "1ype 1",
                "Type 2",
                "Type 3",
                "Type 4"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Type 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.65)"
        },
        {
            "id": "cms26-p1-066",
            "subject": "General Medicine",
            "text": "Infusion of which one of the following antibacterial agents may cause the 'Red Man Syndrome' characterized by rapid onset of erythematous rash and pruritus on the head, face, neck and upper trunk?",
            "options": [
                "Vancomycin",
                "Minocycline",
                "Levofloxacin",
                "Metronidazole"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Vancomycin.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.66)"
        },
        {
            "id": "cms26-p1-067",
            "subject": "General Medicine",
            "text": "Which one of the following can be classically elicited in a patient of Staphylococcal scalded skin syndrome?",
            "options": [
                "Auspitz sign",
                "Koebner phenomenon",
                "Gottron's sign",
                "Nikolsky sign presents with"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Nikolsky sign presents with.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.67)"
        },
        {
            "id": "cms26-p1-068",
            "subject": "General Medicine",
            "text": "generalized muscle rigidity, difficulty in swallowing and laryngeal spasms for the past one week. She has developed trismus over the past 2 days and has a pulse rate of 130 beats/minute and a respiratory rate of 35 breaths/minute on presentation. She gives a history of getting her ears pierced from a roadside jewellery seller 2 weeks ago. What is the most probable diagnosis?",
            "options": [
                "Enteric fever",
                "Pertussis",
                "Diphtheria",
                "Tetanus"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Tetanus.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.68)"
        },
        {
            "id": "cms26-p1-069",
            "subject": "General Medicine",
            "text": "A 25-year-old male presents with complaints of urethral discharge and dysuria for the past 1 week. The discharge was scant and mucoid for a few days but he reports profuse and yellowish discharge since 2 days. Gram staining of the urethral discharge reveals gram-negative intracellular monococci and diplococci. On further questioning, he gives a history of unprotected sexual intercourse 15 days ago. Which one of the following conditions will be your most probable diagnosis ?",
            "options": [
                "Gonorrhea",
                "Chancroid",
                "Syphilis",
                "Lymphogranuloma venereum"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Gonorrhea.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.69)"
        },
        {
            "id": "cms26-p1-070",
            "subject": "General Medicine",
            "text": "A 40-year-old male, upon returning from a beach holiday, noticed a serpiginous, intensely pruritic linear lesion over the dorsum of foot which moved slowly across the skin to reach up to his toes in 5 - 6 days. The most likely clinical diagnosis is :",
            "options": [
                "Cutaneous larva migrans",
                "Anisakiasis",
                "Cutaneous larva currens",
                "Schistosomiasis"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Cutaneous larva migrans.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.70)"
        },
        {
            "id": "cms26-p1-071",
            "subject": "General Medicine",
            "text": "Consider the following statements regarding gas gangrene : 1. It is caused by clostridial species, e.g., Clostridium perfringens. 2. It is characterized by a foul-smelling, painful wound containing serosanguineous discharge and gas bubbles. 3. It requires an aerobic environment and affects sites which are richly supplied with blood. 4. Radical amputation carries a high risk of advancing the infection to healthy tissue and is strictly contraindicated. Which of the statements given above are correct ?",
            "options": [
                "1 and 2",
                "2 and 3",
                "3 and 4",
                "1 and 4"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1 and 2.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.71)"
        },
        {
            "id": "cms26-p1-072",
            "subject": "General Medicine",
            "text": "Which of the following correctly denote(s) the clinical manifestations of diphtheria? 1. Dermatosis characterized by punched-out ulcerative lesions with necrotic sloughing 2. Dysphonia, dysphagia and headache 3. Myocarditis, cardiac arrhythmias and congestive heart failure 4. Massive tonsillar, submandibular and paratracheal oedema presenting as bull-neck' appearance Select the correct answer using the code given below :",
            "options": [
                "1 only",
                "1 and 3 only",
                "2 and 3 only",
                "1, 2, 3 and 4"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 1, 2, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.72)"
        },
        {
            "id": "cms26-p1-073",
            "subject": "General Medicine",
            "text": "Which one of the following is the vector for Leishmania donovani, the causative organism of Visceral Leishmaniasis ?",
            "options": [
                "Tsetse fly",
                "Sandfly",
                "Anopheles mosquito",
                "Reduviid bug"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Sandfly.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.73)"
        },
        {
            "id": "cms26-p1-074",
            "subject": "General Medicine",
            "text": "Casal's Necklace is a characteristic erythema seen in deficiency of which one of the following vitamins?",
            "options": [
                "Thiamin",
                "Riboflavin",
                "Niacin",
                "Pyridoxine"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Niacin.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.74)"
        },
        {
            "id": "cms26-p1-075",
            "subject": "General Medicine",
            "text": "Wickham's striae are typically seen in which one of the following diseases?",
            "options": [
                "Iron-deficiency anemia",
                "Psoriasis",
                "Lichen planus",
                "Pityriasis versicolor"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Lichen planus.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.75)"
        },
        {
            "id": "cms26-p1-076",
            "subject": "General Medicine",
            "text": "Consider the following statements regarding Molluscum contagiosum : 1. It is caused by Papilloma virus skin infection. 2. It occurs frequently in immunosuppressed patients. 3. Lesions are dome-shaped, umbilicated, skin-coloured papules with central punctum. 4. Gently squeezing the lesions with forceps after bathing can hasten resolution. Which of the statements given above are correct?",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 2, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.76)"
        },
        {
            "id": "cms26-p1-077",
            "subject": "General Medicine",
            "text": "Which one of the following refers to the 79. appearance of punctate bleeding spots on scraping the surface of a skin lesion?",
            "options": [
                "Punshi's sign",
                "Barnett's sign",
                "Gottron's sign",
                "Auspitz's sign"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Auspitz's sign.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.77)"
        },
        {
            "id": "cms26-p1-078",
            "subject": "General Medicine",
            "text": "Consider the following statements regarding Complex Regional Pain Syndrome (CRPS) : 1. Type 1 CRPS may be precipitated by a traumatic event such as a fracture. 2. Type 1 CRPS is associated with peripheral nerve damage. Type 2 CRPS is associated with peripheral nerve damage. 4. Budapest criteria are used for diagnosis of CRPS. Which of the statements given above are correct?",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 1, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.78)"
        },
        {
            "id": "cms26-p1-079",
            "subject": "General Medicine",
            "text": "Consider the following statements regarding Dual X-ray Absorptiometry (DXA) : 1. DXA is used to measure bone mineral density. 2. It works on the principle that calcium in bone attenuates passage of X-rays through the tissue in proportion to the amount of mineral present. 3. Osteoporosis is defined to be present when the T-score lies between (-1•0) and below (+2•5). 4. Co-existing conditions, e.g., aortic calcification or degenerative disc disease can cause high bone mineral density even in the presence of osteoporosis. Which of the statements given above are correct?",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1, 2 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.79)"
        },
        {
            "id": "cms26-p1-080",
            "subject": "General Medicine",
            "text": "Which of the following classical disease-modifying anti-rheumatic drugs is/are considered safe for use during pregnancy? 1. Methotrexate 2. Sulfasalazine 3. Hydroxychloroquine 4. Leflunomide Select the correct answer using the code given below :",
            "options": [
                "1 only",
                "1 and 3 only",
                "2 and 3",
                "1, 3 and 4"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.80)"
        },
        {
            "id": "cms26-p1-081",
            "subject": "General Medicine",
            "text": "Finkelstein's sign/test is done to diagnose 84. which one of the following conditions?",
            "options": [
                "Adhesive capsulitis",
                "Golfer's elbow",
                "Trochanteric bursitis",
                "de Quervain's tenosynovitis"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — de Quervain's tenosynovitis.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.81)"
        },
        {
            "id": "cms26-p1-082",
            "subject": "General Medicine",
            "text": "Which of the following are 'first-rank' symptoms of acute schizophrenia? 1. Auditory hallucinations 2. Broadcasting of thoughts 3. Memory loss 4. Delusional perceptions Select the correct answer using the code given below :",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1, 2 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.82)"
        },
        {
            "id": "cms26-p1-083",
            "subject": "General Medicine",
            "text": "A 44-year-old woman has fear of contamination leading to her repeated hand-washing. With regard to her management, consider the following statements : 1. Diagnosis is made on the basis of history. 2. The disorder responds to antidepressant drugs. 3. Patients may be subjected to cognitive behaviour therapy. 4. Admission to a psychiatry ward is mandatory. Which of the statements given above is/are correct ?",
            "options": [
                "1,2 and 3",
                "4 only",
                "3 and 4",
                "1 only"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1,2 and 3.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.83)"
        },
        {
            "id": "cms26-p1-084",
            "subject": "General Medicine",
            "text": "Consider the following statements with regard to point mutations : 1. If a purine is replaced by another purine, it is called 'transition'. 2. If a purine is replaced by a pyrimidine, it is called 'transversion'. 3. If a pyrimidine is replaced by another pyrimidine, it is called 'transversion'. Which of the statements given above are correct?",
            "options": [
                "1 and 2 only",
                "2 and 3 only",
                "1 and 3 only",
                "1, 2 and 3"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1 and 2 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.84)"
        },
        {
            "id": "cms26-p1-085",
            "subject": "General Medicine",
            "text": "Which one of the following correctly denotes a flat, coloured lesion, < 2 cm in diameter, not raised above the surface of the surrounding skin ?",
            "options": [
                "Macule",
                "Patch",
                "Papule",
                "Nodule"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Macule.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.85)"
        },
        {
            "id": "cms26-p1-086",
            "subject": "General Medicine",
            "text": "Which one of the following terms correctly denotes the mechanism and phenotypic changes that are not a result of variation in the underlying DNA sequence, but are caused by secondary modifications of DNA or histones in response to other heritable or environmental influences ?",
            "options": [
                "Pleiotropy",
                "Epigenetics",
                "Co-dominance",
                "Epistasis"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Epigenetics.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.86)"
        },
        {
            "id": "cms26-p1-087",
            "subject": "General Medicine",
            "text": "'Latrodectism', characterized by local pain and sweating, is caused by the bite of which one of the following animals?",
            "options": [
                "Widow spider",
                "King cobra",
                "Lonomia caterpillar",
                "Solenopsis ants"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Widow spider.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.87)"
        },
        {
            "id": "cms26-p1-088",
            "subject": "General Medicine",
            "text": "A farmer was suspected of some unknown substance poisoning, as he presented with bronchorrhoea, sweating and excessive salivation. Examination revealed bradycardia with bilateral miosis. Consider the following statements regarding his poisoning : 1. The symptoms represent Cholinergic Syndrome. 2. Activation of Acetylcholinesterase (AChE) enzyme is the underlying mechanism. 3. Intravenous Atropine should be given for treatment. Which of the statements given above is/are correct ?",
            "options": [
                "1 and 2",
                "2 and 3",
                "1 and 3",
                "3 only"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 3 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.88)"
        },
        {
            "id": "cms26-p1-089",
            "subject": "General Medicine",
            "text": "Which of the following pairs of parasites and associated clinical manifestations are correct? 1. Ancylostoma Anemia duodenale 2. Ascaris Löffler Syndrome lumbricoides 3. Loa loa Katayama Fever 4. Trichinella Myositis spiralis Select the answer using the code given below :",
            "options": [
                "1, 2 and 4",
                "2, 3 and 4",
                "1, 3 and 4",
                "1, 2 and 3 Anti"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1, 2 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.89)"
        },
        {
            "id": "cms26-p1-090",
            "subject": "General Medicine",
            "text": "Which of the following features are present in Locked-in syndrome? 1. Cerebral cortex is intact. 2. Bilateral motor tracts are damaged 3. Some response to verbal stimuli may be present. 4. Limb movement occurs in response to noxious stimuli. Select the correct answer using the code given below :",
            "options": [
                "1 and 4",
                "1 and 2 only",
                "2, 3 and 4",
                "1, 2 and 3"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 1, 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.90)"
        },
        {
            "id": "cms26-p1-091",
            "subject": "General Medicine",
            "text": "A 26-year-old female complains of severe 93. fatigue and myalgia. Examination reveals pallor and mild splenomegaly. Haematological investigations are shown below : Haemoglobin - 10 g/dL Peripheral smear - Microcytic hypochromic picture with anisocytosis Reticulocyte count - 5% Serum ferritin - 300 microgram/L What is the most likely underlying diagnosis?",
            "options": [
                "Iron deficiency",
                "Folic acid deficiency",
                "Vitamin B12 deficiency",
                "B-Thalassemia 94."
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — B-Thalassemia 94..",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.91)"
        },
        {
            "id": "cms26-p1-092",
            "subject": "General Medicine",
            "text": "Which of the following infectious agents are associated with the development of lymphoid malignancies ? 1. HIV 2. Hepatitis B Hepatitis C Select the correct answer using the code given below :",
            "options": [
                "1, 2 and 3",
                "1 and 2 only",
                "1 and 3 only",
                "2 and 3 only"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1, 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.92)"
        },
        {
            "id": "cms26-p1-093",
            "subject": "General Medicine",
            "text": "Which of the following statements regarding Blood component transfusion related acute lung injury are correct? 1. Transfusion related acute lung injury (TRALI) usually manifests within 6 hours of transfusion. 2. Risk factors for TRALI include high titre anti-HLA class II antibodies in donor plasma. 3. TRALI due to cytokines or chemokines can occur even in the absence of HLA mediated interactions. Select the answer using the code given below :",
            "options": [
                "1, 2 and 3",
                "1 and 2 only",
                "1 and 3 only",
                "2 and 3 only"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1, 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.93)"
        },
        {
            "id": "cms26-p1-094",
            "subject": "General Medicine",
            "text": "Match List I with List II and select the correct answer using the code given below the lists: List I List II (Drug) (Mechanism of action) A. Aspirin 1. Thrombolytic B. Enoxaparin 2. Antiplatelet C. Dabigatran 3. Anticoagulant D. Alteplase 4. Direct thrombin inhibitor Code : B C D",
            "options": [
                "2 4 1",
                "2 4 3 1",
                "1 4 2",
                "1 4 2"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 2 4 1.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.94)"
        },
        {
            "id": "cms26-p1-095",
            "subject": "General Medicine",
            "text": "cough and noisy breathing of 2 days' duration. He has a history of running nose and some fever for the preceding 3 - 4 days. Examination reveals respiratory rate of 40 per min, subcostal retractions and stridor. The most important step in the management is :",
            "options": [
                "Nebulized adrenaline",
                "Nebulized salbutamol",
                "Subcutaneous adrenaline",
                "Intravenous hydrocortisone"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Nebulized adrenaline.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.95)"
        },
        {
            "id": "cms26-p1-096",
            "subject": "General Medicine",
            "text": "A 3-year-old boy presents to the emergency room with seizures. He has been receiving oral phenytoin since the age of 6 months and has a history of epileptic spasms despite therapy. Examination reveals some hypopigmented lesions over the chest. MRI brain shows subependymal nodules. Which one of the following is the best anti-epileptic drug for him after stabilization in the emergency room ?",
            "options": [
                "Oral Phenytoin",
                "Oral Zonisamide",
                "Oral Topiramate",
                "Oral Vigabatrin"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Oral Vigabatrin.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.96)"
        },
        {
            "id": "cms26-p1-097",
            "subject": "Pediatrics",
            "text": "A 3-year-old boy is brought with barking 97. A 10-year-old girl presents to the emergency with high grade fever of 2-weeks duration and rashes over lower limbs for the last 7 days. Examination reveals mild pallor, generalized petechiae and hepatosplenomegaly. Investigations reveal : Hemoglobin 9 g/dL, total leucocyte count 2100/mm®, platelet count 20,000/mm®, peripheral smear shows pancytopenia, SGOT 50 IU/dL, SGPT 64 IU/dL, serum ferritin 1200 ug/L, serum fibrinogen 100 mg/dL and serum triglycerides of 350 mg/dL. The most likely diagnosis is :",
            "options": [
                "Aplastic anemia",
                "Immune thrombocytopenic purpura",
                "Hemophagocytic lymphohistiocytosis",
                "Acute promyelocytic leukemia"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Hemophagocytic lymphohistiocytosis.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.97)"
        },
        {
            "id": "cms26-p1-098",
            "subject": "Pediatrics",
            "text": "A 5-year-old boy, started on induction chemotherapy for acute lymphoblastic leukemia, develops acute abdominal pain on day 14 of chemotherapy. On abdominal examination, there is marked abdominal tenderness and Cullen's sign is positive. The most likely chemotherapeutic drug which can be implicated is :",
            "options": [
                "Vincristine",
                "Daunorubicin",
                "L-asparaginase",
                "Methotrexate"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — L-asparaginase.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.98)"
        },
        {
            "id": "cms26-p1-099",
            "subject": "Pediatrics",
            "text": "A 5-year-old boy who was started on treatment for Burkitt lymphoma develops acute onset respiratory distress and decreased urine output. Investigations reveal : Hb 8 g/dL, TLC 15000/mm®, platelet count 1 lakh/mm?, serum potassium 6￾5 mEq/L, corrected serum calcium 6•7 mg/dL and serum creatinine 2 mg/dL. The most important drug for emergency management is :",
            "options": [
                "Dexamethasone",
                "Broad-spectrum antibiotics",
                "Rasburicase",
                "Folinic acid rescue"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Rasburicase.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.99)"
        },
        {
            "id": "cms26-p1-100",
            "subject": "Pediatrics",
            "text": "Consider the following statements regarding human milk banking : 1. The banks accept voluntary milk donations from lactating women who are given nominal payments governed by law. 2. Donor mothers are screened via blood similar to blood donation. 3. Pasteurized donor milk reduces the chances of NEC in preterm neonates. 4. Pasteurized donor milk is non-inferior to fresh mother's own milk (MOM). Which of the statements given above are correct ?",
            "options": [
                "1, 2 and 3",
                "2 and 3 only",
                "3 and 4 only",
                "1, 2, 3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 2 and 3 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.100)"
        },
        {
            "id": "cms26-p1-101",
            "subject": "Pediatrics",
            "text": "A term neonate weighing 2 kg, delivered to a primigravida mother through vaginal route and through clear liquor, is found having gasping respiratory efforts after performing the initial steps in the delivery room. The next step in resuscitation is :",
            "options": [
                "Initiate positive pressure ventilation with bag and mask using 30% oxygen",
                "Intubate and initiate positive pressure ventilation using 30% oxygen",
                "Initiate positive pressure ventilation with bag and mask using room air",
                "Intubate and initiate positive pressure ventilation using room air"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Initiate positive pressure ventilation with bag and mask using room air.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.101)"
        },
        {
            "id": "cms26-p1-102",
            "subject": "Pediatrics",
            "text": "A newborn delivered at 37 weeks gestation and birth weight 2:7 kg, presents at 12 h of life with bilious vomiting. On examination, RR is 36/m, HR is 110/m, CRT is < 3s, and there is abdominal distention. Abdominal radiograph reveals multiple air-fluid levels with absent distal gas pattern. The most likely etiology is :",
            "options": [
                "Malrotation leading to volvulus",
                "Congenital hypertrophic pyloric stenosis",
                "Jejunal-ileal atresia",
                "Necrotizing enterocolitis"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Jejunal-ileal atresia.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.102)"
        },
        {
            "id": "cms26-p1-103",
            "subject": "Pediatrics",
            "text": "tests for HIV, and Hepatitis B and C, 103. Consider the following statements regarding the management of trachea-esophageal fistula in neonates : 1. The baby should be nursed in prone position. 2. The neonate should be kept nil per orally and started on intravenous fluids. 3. The neonate needs continuous oral suction using a slow suction device. 4. Surgery should be planned once the neonate attains 25 kg weight. Which of the statements given above are correct?",
            "options": [
                "1 and 2 only",
                "1, 2 and 3",
                "2 and 3 only",
                "3 and 4"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 2 and 3 only.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.103)"
        },
        {
            "id": "cms26-p1-104",
            "subject": "Pediatrics",
            "text": "An apparently well male neonate delivered by vaginal route in hospital is discharged on day 2 of life. He is brought to the outpatient department on day 4 of life as the mother complains of pink staining of his diapers. There is no bleeding from urethra or per rectum noticed during examination, and urine dipstick test for RBCs is negative. The baby is appearing playful and active. The most likely etiology of pink staining of diapers is :",
            "options": [
                "Porphyria",
                "Urate crystals in urine",
                "Hemoglobinuria",
                "Hematuria"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Urate crystals in urine.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.104)"
        },
        {
            "id": "cms26-p1-105",
            "subject": "Pediatrics",
            "text": "A preterm neonate is brought to the emergency and the body temperature is noted to be 32°C. Which one of the following metabolic complications is unlikely?",
            "options": [
                "Metabolic alkalosis",
                "Hypoglycemia",
                "Hyperbilirubinemia",
                "Hypoxemia"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Metabolic alkalosis.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.105)"
        },
        {
            "id": "cms26-p1-106",
            "subject": "Pediatrics",
            "text": "A 3-year-old boy is brought to the outpatient department with complaints of developmental delay. He can feed himself a biscuit, can draw a line, can climb steps, and only says bisyllables. Which one of the following developmental screening tools is not suitable for him ?",
            "options": [
                "Phatak's Baroda Screening Test",
                "Ages and Stages Questionnaire",
                "Trivandrum Development Screening Chart",
                "Denver II"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Phatak's Baroda Screening Test.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.106)"
        },
        {
            "id": "cms26-p1-107",
            "subject": "Pediatrics",
            "text": "An 8-year-old girl is provided a few cubes and asked to create the structure in the image provided. If she can create the Structure A, but cannot make the Structure B, her developmental quotient (DQ) in the fine motor domain is : B.",
            "options": [
                "50",
                "62￾5",
                "75",
                "100"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 62￾5.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.107)"
        },
        {
            "id": "cms26-p1-108",
            "subject": "Pediatrics",
            "text": "A 2-year-old boy was brought to the emergency when his mother noticed that he had developed dusky appearance and lethargy over the past 6 - 8 hours. The child had been prescribed some medicine for vomiting by a local practitioner. Examination revealed normal sized pupils reacting to light, GCS 9, and shallow breathing with cyanosis. Arterial blood gas revealed a Pa02 of 80 mmHg and SpO2 of 60%. Which one of the following drugs may be implicated ?",
            "options": [
                "Domperidone",
                "Granisetron",
                "Aprepitant",
                "Metoclopramide"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Metoclopramide.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.108)"
        },
        {
            "id": "cms26-p1-109",
            "subject": "Pediatrics",
            "text": "A 12-year-old boy is brought to the emergency in an unconscious state with a history of shallow breathing and increasing drowsiness noticed for two hours. He is noticed to have a dry mouth, cold extremities, is limp and has pin point pupils. The emergency physician suspects poisoning. Which one of the following antidotes should be administered?",
            "options": [
                "Flumazenil",
                "Adrenaline",
                "Pralidoxime",
                "Naloxone"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Naloxone.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.109)"
        },
        {
            "id": "cms26-p1-110",
            "subject": "Pediatrics",
            "image_url": "/static/exam_images/cms26_p1_q110_xray.png",
            "text": "A neonate is noted to have bilious vomiting at 6 hours of life with abdominal distention. An X-ray is ordered (see image). The most likely diagnoșis is :",
            "options": [
                "Pyloric stenosis",
                "Esophageal atresia",
                "Duodenal atresia",
                "Hirschsprung's disease"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Duodenal atresia.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.110)"
        },
        {
            "id": "cms26-p1-111",
            "subject": "Pediatrics",
            "text": "A 6-year-old boy is brought with complaints of involuntary, non-rhythmic, jerky movements of upper limbs and snorting sounds, noticed for the past 12 months. His MRI brain and EEG are normal. The child was mocked at by classmates in school and he stopped attending classes for the past 6 months. His ASLO titres and serum ceruloplasmin are non-contributory. The ideal therapy would be a trial of :",
            "options": [
                "Oral Clonidine",
                "Oral Methylphenidate",
                "Oral Benzodiazepines",
                "Oral Olanzapine"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Oral Clonidine.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.111)"
        },
        {
            "id": "cms26-p1-112",
            "subject": "Pediatrics",
            "text": "A 4-year-old unimmunized HIV-positive child on antiretroviral therapy for the last 2 years and weighing 15 kg is brought for vaccination. His records reveal a recent CD4 count of 750/mm, with no evidence of any opportunistic infections in the past. Which of the following statements are applicable to this child ? 1. Recombinant Hepatitis B vaccine can be safely administered. 2. MMR vaccine is always contraindicated. 3. BCG may be administered if chest radiograph is normal. IPV is preferred over OPV. Select the correct answer using the code given below :",
            "options": [
                "1 and 2",
                "2 and 3",
                "1 and 4",
                "2 and 4"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 1 and 4.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.112)"
        },
        {
            "id": "cms26-p1-113",
            "subject": "Pediatrics",
            "text": "As per the National Immunization Schedule, PCV (Pneumococcal Conjugate Vaccine) is offered at :",
            "options": [
                "6 weeks, 10 weeks and 14 weeks",
                "6 weeks and 14 weeks",
                "6 weeks, 10 weeks and 9 months",
                "6 weeks, 14 weeks, 9 months"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 6 weeks, 14 weeks, 9 months.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.113)"
        },
        {
            "id": "cms26-p1-114",
            "subject": "Pediatrics",
            "text": "Which one of the following vaccines is an exception to the principle \"At least 4 weeks interval is needed between two doses of the same vaccine to ensure adequate immune responseằ_",
            "options": [
                "Rabies vaccine",
                "HPV vaccine",
                "Varicella vaccine",
                "Hepatitis B vaccine"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Rabies vaccine.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.114)"
        },
        {
            "id": "cms26-p1-115",
            "subject": "Pediatrics",
            "text": "Administration of immunoglobulins interferes with the response to live vaccines, except :",
            "options": [
                "Measles vaccine",
                "Rubella vaccine",
                "Oral typhoid vaccine",
                "Mumps vaccine"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Oral typhoid vaccine.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.115)"
        },
        {
            "id": "cms26-p1-116",
            "subject": "Pediatrics",
            "text": "A 14-year-old boy is reported by his neighbour to the police for repeated aggressive activities including beating up children in the neighbourhood. The boy's neighbour also noticed that he also snorts heroin sometimes. He will be categorized legally as suffering from :",
            "options": [
                "Oppositional defiant disorder",
                "Conduct disorder",
                "Juvenile delinquency",
                "Drug addiction"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Juvenile delinquency.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.116)"
        },
        {
            "id": "cms26-p1-117",
            "subject": "Pediatrics",
            "text": "As per the National Vector Borne Disease Control Programme, the first-line agent for treatment of Kala-azar leishmaniasis) is :",
            "options": [
                "Amphotericin B, liposomal, IV, single dose",
                "Sodium stibogluconate, IV, 30-day regimen",
                "Oral Miltefosine, 28-day regimen",
                "Amphotericin B deoxycholate, IV, 30 doses"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Amphotericin B, liposomal, IV, single dose.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.117)"
        },
        {
            "id": "cms26-p1-118",
            "subject": "Pediatrics",
            "text": "Which one of the following illnesses is not covered under the Rashtriya Bal Swasthya Karyakram ?",
            "options": [
                "Childhood cancer",
                "Down syndrome",
                "Goitre",
                "Rheumatic heart disease"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Childhood cancer.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.118)"
        },
        {
            "id": "cms26-p1-119",
            "subject": "Pediatrics",
            "text": "A 2-year-old child is brought with complaints of not growing well. On examination, he weighs 8-1 kg, height 80 cm (WFL score between 0 and - 2 SD), has a mid-arm circumference (MUAC) of 11•5 cm and both his palms are white. There is no edema of the feet. As per IMNCI, he will be classified as :",
            "options": [
                "No acute malnutrition and anemia",
                "No acute malnutrition and severe anemia",
                "Moderate acute malnutrition and anemia",
                "Moderate acute malnutrition and severe anemia"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Moderate acute malnutrition and severe anemia.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.119)"
        },
        {
            "id": "cms26-p1-120",
            "subject": "Pediatrics",
            "text": "A 2-year-old previously unimmunized girl is brought with poor feeding and fever for 6 days. On day 4 of fever, her mother noticed a maculopapular reddish rash starting from the face and spreading over the neck, chest, arms and trunk over the next one day and she has developed extensive mouth ulcers. The child (visceral has a mid-arm circumference of 11 cm but no edema. As per IMNCI, she will be classified as :",
            "options": [
                "Measles with eye or mouth complications",
                "Measles",
                "Severe complicated measles",
                "Measles with severe acute malnutrition SPACE FOR ROUGH WORK SPACE FOR ROUGH WORK SPACE FOR ROUGH WORK SPACE FOR ROUGH WORK"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Severe complicated measles.",
            "citation": "UPSC CMS 2026 Paper-I (NTDC-O-KPMS Series-A Q.120)"
        }
    ],
    "upsc-cms-2026-paper-2-authentic": [
        {
            "id": "cms26-p2-001",
            "subject": "General Surgery",
            "text": "A 50-year-old destitute is brought to the emergency with a foul-smelling wound on his left foot. On examination, the wound is seen to have maggots with a lot of necrotic tissue. What is the class of this wound according to the CDC wound classification?",
            "options": [
                "Class 1",
                "Class 2",
                "Class 3",
                "Class 4"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Class 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.1)"
        },
        {
            "id": "cms26-p2-002",
            "subject": "General Surgery",
            "text": "Which one of the following is not a wound prone to the development of tetanus?",
            "options": [
                "Compound fracture of tibia",
                "Wound on forearm contaminated with soil",
                "Donor site of a split-thickness skin graft",
                "Dog bite over abdominal wall"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Donor site of a split-thickness skin graft.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.2)"
        },
        {
            "id": "cms26-p2-003",
            "subject": "General Surgery",
            "text": "All of the following are features of a major surgical site infection (SSI), except",
            "options": [
                "significant amount of pus",
                "delayed return home",
                "excessive pain at the surgical site",
                "patients being systemically ill"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — excessive pain at the surgical site.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.3)"
        },
        {
            "id": "cms26-p2-004",
            "subject": "General Surgery",
            "text": "An infant is brought to the clinic by the parents with the history of a swelling in the neck since birth. On examination, the swelling is found to be soft, partially compressible and brilliantly trans- illuminant. The most likely diagnosis is",
            "options": [
                "sternomastoid tumour",
                "branchial cyst",
                "thyroglossal cyst",
                "cystic hygroma"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — cystic hygroma.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.4)"
        },
        {
            "id": "cms26-p2-005",
            "subject": "General Surgery",
            "text": "Which one of the following statements regarding inherited cancer syndromes is not correct?",
            "options": [
                "Pituitary tumours are seen in MEN type 1.",
                "Brain tumours are seen in Li-Fraumeni syndrome.",
                "Breast cancer is seen in FAP syndrome.",
                "Prostate cancer is seen in familial breast cancer syndrome."
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Breast cancer is seen in FAP syndrome..",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.5)"
        },
        {
            "id": "cms26-p2-006",
            "subject": "General Surgery",
            "text": "Which of the following are the causes of secondary lymphoedema? 1. Trauma 2. Deep venous thrombosis 3. Fungal infection 4. Viral infection Select the correct answer using the code given below.",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "1, 3 and ą",
                "2, 3 and 4"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1, 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.6)"
        },
        {
            "id": "cms26-p2-007",
            "subject": "General Surgery",
            "text": "The classical presentation of an acute embolic occlusion in a limb includes all of the following, except",
            "options": [
                "pain",
                "purple discoloration",
                "paralysis",
                "pulselessness"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — purple discoloration.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.7)"
        },
        {
            "id": "cms26-p2-008",
            "subject": "General Surgery",
            "image_url": "/static/exam_images/cms26_p2_q8_ulcer.png",
            "text": "The typical ulcer as shown in the following diagram is seen in",
            "options": [
                "syphilis",
                "squamous cell carcinoma",
                "tuberculosis",
                "basal cell carcinoma"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — tuberculosis.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.8)"
        },
        {
            "id": "cms26-p2-009",
            "subject": "General Surgery",
            "text": "A patient is undergoing a surgery for removal of a benign tumour from the parotid gland. Which one of the following structures should be preserved during this surgery?",
            "options": [
                "Facial artery",
                "Auriculotemporal nerve",
                "Zygomatic artery",
                "Facial nerve"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Facial nerve.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.9)"
        },
        {
            "id": "cms26-p2-010",
            "subject": "General Surgery",
            "text": "A 52-year-old carpenter presents with the history of a persistent non-healing ulcer on his lower alveolus. He is a smoker for last 30 years and also chews tobacco. What is the next most appropriate step in the management?",
            "options": [
                "X-ray mandible",
                "Edge biopsy of ulcer",
                "Local gum paint (astringent + analgesic)",
                "Systemic antibiotics"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Edge biopsy of ulcer.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.10)"
        },
        {
            "id": "cms26-p2-011",
            "subject": "General Surgery",
            "image_url": "/static/exam_images/cms26_p2_q11_scan.png",
            "text": "A 40-year-old female presents with symptoms of heat intolerance, excessive sweating and weight loss since 10-12 months. After clinical examination, the surgeon orders an investigation which is as shown in the image. The scan shown below is a/an",
            "options": [
                "MRI scan",
                "non-contrast CT scan",
                "radionuclide scan",
                "PET scan"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — radionuclide scan.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.11)"
        },
        {
            "id": "cms26-p2-012",
            "subject": "General Surgery",
            "text": "A 29-year-old lady presents with a history of discharge from the nipple of the left breast since 1 month duration. Which one of the following is not warranted in the initial assessment of this patient?",
            "options": [
                "Clinical examination",
                "Histo / Cytopathology",
                "Mammography",
                "Ultrasonography"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Mammography.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.12)"
        },
        {
            "id": "cms26-p2-013",
            "subject": "General Surgery",
            "text": "A 45-year-old lady presents with a hard lump in the left breast. On examination, the lump is found to be 4 cm × 6 cm in size, not fixed to the skin, but fixed to the underlying pectoralis major muscle. The T stage of this is",
            "options": [
                "cT4a",
                "CT3",
                "cT4b",
                "cT2"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — CT3.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.13)"
        },
        {
            "id": "cms26-p2-014",
            "subject": "General Surgery",
            "text": "Which one of the following statements regarding choledochal cyst is not correct?",
            "options": [
                "Choledochal cysts are congenital dilatations of intra- and/or extra- hepatic biliary system.",
                "Majority of patients are diagnosed after 10 years of age.",
                "It is associated with an increased risk of developing cholangio- carcinoma.",
                "Radical excision of the cyst is the treatment of choice."
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Majority of patients are diagnosed after 10 years of age..",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.14)"
        },
        {
            "id": "cms26-p2-015",
            "subject": "General Surgery",
            "text": "Which one of the following is the most common benign liver lesion?",
            "options": [
                "Hepatic adenoma",
                "Hemangioma",
                "Focal nodular hyperplasia",
                "Simple liver cyst"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Hemangioma.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.15)"
        },
        {
            "id": "cms26-p2-016",
            "subject": "General Surgery",
            "text": "The line diagram shows the cross- section of bowel intussusception. The part marked with an asterisk is called as",
            "options": [
                "apex",
                "intussusceptum",
                "base",
                "intussuscipiens"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — intussusceptum.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.16)"
        },
        {
            "id": "cms26-p2-017",
            "subject": "General Surgery",
            "text": "Which one of the following statements regarding peptic ulceration is not correct?",
            "options": [
                "Most peptic ulcers are caused by Helicobacter pylori or NSAIDs.",
                "Gastric ulcers are more common than duodenal ulcers.",
                "Gastric ulcers may be malignant.",
                "Gastric antisecretory agents and H. pylori eradication therapy are the mainstays of treatment."
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Gastric ulcers are more common than duodenal ulcers..",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.17)"
        },
        {
            "id": "cms26-p2-018",
            "subject": "General Surgery",
            "text": "A trainee surgeon is performing his/her first cholecystectomy. The area marked with an asterisk in the diagram represents",
            "options": [
                "Rouviere's area",
                "Bismuth's triangle",
                "Calot's triangle",
                "area of Lund"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Calot's triangle.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.18)"
        },
        {
            "id": "cms26-p2-019",
            "subject": "General Surgery",
            "image_url": "/static/exam_images/cms26_p2_q19_pringle.png",
            "text": "The manoeuvre (marked with an asterisk) shown in the following image is",
            "options": [
                "Mattox",
                "Kocher",
                "Shoe-shine",
                "Pringle"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Pringle.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.19)"
        },
        {
            "id": "cms26-p2-020",
            "subject": "General Surgery",
            "text": "Which of the following are the common complications after splenectomy? 1. Pancreatic fistula 2. Thrombocytopenia 3. Opportunistic infection 4. Left basal atelectasis Select the correct answer using the code given below.",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 1, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.20)"
        },
        {
            "id": "cms26-p2-021",
            "subject": "General Surgery",
            "text": "A 42-year-old lady underwent laparoscopic cholecystectomy, which was uneventful other than some spillage of bile and gallstones during dissection. Postoperatively the patient was fine but she started complaining of right shoulder tip pain and developed high grade fever on the 3rd postoperative day. Her pulse was found to be 110/min and RR 20/min. The most likely diagnosis is",
            "options": [
                "ascending cholangitis",
                "liver abscess",
                "right subdiaphragmatic abscess",
                "DVT and pulmonary embolism"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — right subdiaphragmatic abscess.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.21)"
        },
        {
            "id": "cms26-p2-022",
            "subject": "General Surgery",
            "image_url": "/static/exam_images/cms26_p2_q22_hernia.png",
            "text": "A 40-year-old male patient has undergone a surgical procedure for a swelling in his left groin. The image of the procedure is as shown. What procedure has been performed?",
            "options": [
                "Shouldice repair",
                "Lichtenstein's repair",
                "Bassini's repair",
                "Desarda's repair"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Lichtenstein's repair.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.22)"
        },
        {
            "id": "cms26-p2-023",
            "subject": "General Surgery",
            "text": "A patient of blunt trauma to the abdomen is being explored in the emergency. Intraoperatively a non-expanding haematoma is seen lifting the descending colon. What is the appropriate management of this patient?",
            "options": [
                "Haematoma to be explored, nothing to be done to the colon",
                "Haematoma to be explored, the colon to be resected",
                "Haematoma not to be explored, nothing to be done to the colon",
                "Haematoma not to be explored, the colon to be resected"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Haematoma not to be explored, nothing to be done to the colon.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.23)"
        },
        {
            "id": "cms26-p2-024",
            "subject": "General Surgery",
            "image_url": "/static/exam_images/cms26_p2_q24_kidney.png",
            "text": "The clinical condition shown in the image is",
            "options": [
                "malrotated kidney",
                "malascended kidney",
                "doughnut kidney",
                "horseshoe kidney"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — horseshoe kidney.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.24)"
        },
        {
            "id": "cms26-p2-025",
            "subject": "General Surgery",
            "image_url": "/static/exam_images/cms26_p2_q25_monro.png",
            "text": "The principle of adaptation shown in the following diagram is explained by Venous Arterial Brain Mass CSF blood blood - Skull",
            "options": [
                "Moynihan's aphorism",
                "Goodsall's rule",
                "Monro-Kellie doctrine",
                "Cushing's law"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Monro-Kellie doctrine.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.25)"
        },
        {
            "id": "cms26-p2-026",
            "subject": "General Surgery",
            "text": "Astrocytomas are associated with all of the following syndromes, except",
            "options": [
                "neurofibromatosis type 1",
                "neurofibromatosis type 2",
                "Cowden's disease",
                "Li-Fraumeni syndrome"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — neurofibromatosis type 2.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.26)"
        },
        {
            "id": "cms26-p2-027",
            "subject": "General Surgery",
            "image_url": "/static/exam_images/cms26_p2_q27_crico.png",
            "text": "The procedure shown in the following images is",
            "options": [
                "elective tracheostomy",
                "emergency tracheostomy",
                "emergency cricothyroidotomy",
                "percutaneous tracheostomy"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — emergency cricothyroidotomy.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.27)"
        },
        {
            "id": "cms26-p2-028",
            "subject": "General Surgery",
            "text": "Consider the following statements regarding flail chest : 1. Three or more ribs are fractured at two or more places. 2. The chest wall shows paradoxical motion. 3. An X-ray chest AP view is the gold standard for diagnosis. 4. Treatment involves oxygen support, analgesia and physiotherapy. Which of the statements given above are correct?",
            "options": [
                "1, 2 and 3",
                "1, 2 and ą",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1, 2 and ą.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.28)"
        },
        {
            "id": "cms26-p2-029",
            "subject": "General Surgery",
            "text": "All of the following are causes secondary osteoarthritis of the hip, except",
            "options": [
                "trauma",
                "diabetes",
                "Perthes' disease",
                "avascular necrosis"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — diabetes.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.29)"
        },
        {
            "id": "cms26-p2-030",
            "subject": "General Surgery",
            "text": "All of the following are causes of acute red eye, except",
            "options": [
                "keratitis",
                "retinitis",
                "episcleritis",
                "uveitis"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — retinitis.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.30)"
        },
        {
            "id": "cms26-p2-031",
            "subject": "General Surgery",
            "text": "The maximum dose of Lidocaine (without adrenaline) for local anaesthesia is",
            "options": [
                "2 mg/kg",
                "3 mg/kg",
                "4 mg/kg",
                "6 mg/kg"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 3 mg/kg.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.31)"
        },
        {
            "id": "cms26-p2-032",
            "subject": "General Surgery",
            "text": "A young lady is brought to emergency department following stab injury to right chest. She is gasping for breath, with tachypnoea, distended neck veins and tracheal shift to left on examination. There is hyperresonance and absent breath sounds on right hemithorax. The most probable diagnosis is",
            "options": [
                "right simple pneumothorax",
                "right tension pneumothorax",
                "cardiac tamponade",
                "right hydropneumothorax"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — right tension pneumothorax.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.32)"
        },
        {
            "id": "cms26-p2-033",
            "subject": "General Surgery",
            "text": "A 25-year-old motorcycle rider is brought to the emergency with history of motor vehicle accident. On primary survey, he is found to open eyes in response to pain, speaking inappropriate words and localizes pain. His Glasgow Coma Scale",
            "options": [
                "E3 V4 M4",
                "E2 V3 M5",
                "E3 V3 M4",
                "E2 V4 M 5"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — E2 V3 M5.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.33)"
        },
        {
            "id": "cms26-p2-034",
            "subject": "General Surgery",
            "image_url": "/static/exam_images/cms26_p2_q34_lefort.png",
            "text": "The type of fracture marked with arrow heads in the following figure is",
            "options": [
                "Le Fort IV",
                "Le Fort III",
                "Le Fort II",
                "Le Fort I"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Le Fort I.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.34)"
        },
        {
            "id": "cms26-p2-035",
            "subject": "General Surgery",
            "text": "Which of the following are the important parameters to be maintained in a patient with head trauma? 1. MAP 70-80 mm Hg (mean arterial pressure) 2. Intracranial pressure ‹ 20 mm Hg 3. Cerebral perfusion pressure > 60 mm Hg 4. Na > 140 mEq/L Select the correct answer using the code given below.",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 2, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.35)"
        },
        {
            "id": "cms26-p2-036",
            "subject": "General Surgery",
            "text": "Which one of the following imaging modalities imparts the highest dose of ionizing radiation to the patient?",
            "options": [
                "Ultrasound",
                "Chest X-ray",
                "Screening mammography",
                "CT head and neck"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — CT head and neck.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.36)"
        },
        {
            "id": "cms26-p2-037",
            "subject": "General Surgery",
            "text": "Which of the following parameters are assessed during preoperative airway assessment for a surgical patient? 1. Mouth opening 2. Ability to protrude the jaw 3. Thyromental distance 4. Cervicomental distance Select the correct answer using the code given below.",
            "options": [
                "1, 2 and 3",
                "1, 3 and 4",
                "2, 3 and 4",
                "1, 2 and 4"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1, 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.37)"
        },
        {
            "id": "cms26-p2-038",
            "subject": "General Surgery",
            "image_url": "/static/exam_images/cms26_p2_q38_suture.png",
            "text": "The type of suture technique shown in the following diagram is",
            "options": [
                "simple interrupted",
                "mattress",
                "Connell",
                "Donati"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — mattress.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.38)"
        },
        {
            "id": "cms26-p2-039",
            "subject": "General Surgery",
            "text": "Which of the following gastrointestinal secretions normally do not contain bicarbonate? 1. Stomach 2. Saliva 3. Duodenal 4. Ileal Select the correct answer using the code given below.",
            "options": [
                "1, 2 and 3",
                "1 and 3 only",
                "1, 3 and 4",
                "2 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1 and 3 only.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.39)"
        },
        {
            "id": "cms26-p2-040",
            "subject": "General Surgery",
            "text": "A 25-year-old motorcycle rider is brought to the emergency with history of motor vehicle accident. On examination, the patient is tachycardic (pulse 110/min) with a BP of 90 systolic. He has an open wound in the thigh with an estimated blood loss of 1000 mL. What is the severity of haemorrhagic shock this patient is suffering from?",
            "options": [
                "Class 1",
                "Class 2",
                "Class 3",
                "Class 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Class 2.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.40)"
        },
        {
            "id": "cms26-p2-041",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which one of the following sets of vaccines is contraindicated in pregnancy?",
            "options": [
                "Pneumococcal, Hepatitis B, HPV",
                "Rabies, Influenza, Hepatitis A",
                "Varicella, Measles, Rubella",
                "Diphtheria, Influenza, Pneumo- coccal"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Varicella, Measles, Rubella.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.41)"
        },
        {
            "id": "cms26-p2-042",
            "subject": "Obstetrics & Gynaecology",
            "text": "Consider the following statements regarding chorionic villus sampling (CVS) used for prenatal diagnosis : 1. It is done between 15 to 20 weeks of gestation. 2. Amniotic fluid studies give earlier diagnosis of prenatal genetic conditions than chorionic villus sampling. 3. Limb reduction deformity is low when CVS is performed after 9 completed weeks of gestation. 4. Inj. Anti-D 50 microgram should be administered following this procedure in an Rh-negative mother. Which of the statements given above are correct?",
            "options": [
                "2 and 4",
                "1, 2 and 3",
                "1, 3 and 4",
                "3 and 4 only"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 3 and 4 only.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.42)"
        },
        {
            "id": "cms26-p2-043",
            "subject": "Obstetrics & Gynaecology",
            "text": "As per the WHO recommendations, all of the following may be given for active management of third stage of labour, except",
            "options": [
                "Inj. Oxytocin",
                "Inj. Methergine",
                "Tab. Misoprostol",
                "Inj. Carboprost"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Inj. Carboprost.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.43)"
        },
        {
            "id": "cms26-p2-044",
            "subject": "Obstetrics & Gynaecology",
            "text": "Consider the following statements regarding the cause for onset of labour : Statement 1 : Alteration in estrogen-progesterone ratio results in prostaglandin synthesis and onset of labour. Statement 2 : Decreased fetal production of dehydroepiandrosterone sulfate (DHEA-S) and cortisol inhibits the conversion of fetal pregnenolone to progesterone. Which one of the following is correct with respect to the above statements?",
            "options": [
                "Both Statements 1 and 2 are true and Statement 2 is the correct explanation of Statement 1",
                "Both Statements 1 and 2 are true but Statement 2 is not the correct explanation of Statement 1",
                "Statement 1 is true but Statement 2 is false",
                "Statement 1 is false but Statement 2 is true"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Statement 1 is true but Statement 2 is false.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.44)"
        },
        {
            "id": "cms26-p2-045",
            "subject": "Obstetrics & Gynaecology",
            "text": "Consider the following statements regarding the WHO Labour Care Guide for labour monitoring : 1. Active phase starts from 5 cm of cervical dilatation. 2. There is fixed rate for dilatation for every hour of labour in active phase. 3. There are no alert or action lines on the partograph. 4. There is a separate section for intensive monitoring for second stage of labour as well. Which of the statements given above are correct?",
            "options": [
                "1, 2 and 4",
                "1, 3 and 4",
                "2, 3 and 4",
                "1, 2 and 3"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.45)"
        },
        {
            "id": "cms26-p2-046",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which of the following are positive indicators for breech vaginal delivery?",
            "options": [
                "Fetal weight less than 1•5 kg, flexed fetal head, frank breech",
                "Frank breech, fetal weight more than 3￾5 kg, gestational age more than 34 weeks",
                "Frank breech, fetal weight 1•5 kg to 35 kg, gestational age more than 34 weeks",
                "Flexed breech, fetal weight 1•5 kg to 3•5 kg, gestational age more than 34 weeks"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Frank breech, fetal weight 1•5 kg to 35 kg, gestational age more than 34 weeks.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.46)"
        },
        {
            "id": "cms26-p2-047",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which one of the following correctly defines puerperal pyrexia?",
            "options": [
                "Rise in maternal oral temperature of 100•4 °F or more 24 hours apart within first 10 days of delivery",
                "Rise in maternal oral temperature of 101•4 °F or more 24 hours apart within first 10 days of delivery",
                "Rise in maternal oral temperature of 1004 °F or more 24 hours apart within first 7 days of delivery",
                "Rise in maternal oral temperature of 101•4 °F or more 24 hours apart within first 7 days of delivery"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Rise in maternal oral temperature of 100•4 °F or more 24 hours apart within first 10 days of delivery.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.47)"
        },
        {
            "id": "cms26-p2-048",
            "subject": "Obstetrics & Gynaecology",
            "text": "A mother presents on day 8 of normal vaginal delivery with painful left breast, fever with chills. On examination, her left breast is tender and red with raised local temperature. What should be the line of management?",
            "options": [
                "Analgesics and antibiotics, plenty of fluids, breastfeeding continued from right breast",
                "Hot fomentation, restricted fluids, avoid breast- sven bran- feeding from either breast",
                "Antibiotics, incision and drainage, avoid breastfeeding from either breast",
                "Antibiotics, analgesics, restricted fluids, breastfeeding continued from right breast"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Analgesics and antibiotics, plenty of fluids, breastfeeding continued from right breast.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.48)"
        },
        {
            "id": "cms26-p2-049",
            "subject": "Obstetrics & Gynaecology",
            "text": "Consider the following abnormalities in a woman with preeclampsia : 1. Platelet count less than 1 lakh/ cumm 2. Serum creatinine > 1￾1 mg/dL 3. Pulmonary edema 4. Proteinuria > 1 g per day Which of the above describe severe features of preeclampsia?",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "2, 3 and 4",
                "1, 3 and 4"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1, 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.49)"
        },
        {
            "id": "cms26-p2-050",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which one of the following parameters precisely defines grade 3 abruptio placentae?",
            "options": [
                "Moderate vaginal bleeding",
                "Maternal tachycardia",
                "Low fibrinogen level",
                "Intrauterine fetal death"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Intrauterine fetal death.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.50)"
        },
        {
            "id": "cms26-p2-051",
            "subject": "Obstetrics & Gynaecology",
            "text": "A primigravida comes to antenatal clinic for a routine antenatal visit. When should she be screened for diabetes in pregnancy?",
            "options": [
                "At 24 to 28 weeks of pregnancy and/or repeat at 30 to 32 weeks of pregnancy",
                "Early in pregnancy and/or repeat at 24 to 28 weeks of pregnancy",
                "Early in pregnancy and/or repeat at 30 to 32 weeks of pregnancy",
                "At 9 to 11 weeks of pregnancy and/or repeat at 30 to 32 weeks of pregnancy"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Early in pregnancy and/or repeat at 24 to 28 weeks of pregnancy.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.51)"
        },
        {
            "id": "cms26-p2-052",
            "subject": "Obstetrics & Gynaecology",
            "text": "A primigravida comes to antenatal clinic at 6 weeks of pregnancy and mentions that she is a known case of epilepsy and is taking antiepileptic drug tablet Valproate since two years. What will be your next step regarding her medication?",
            "options": [
                "Continue Valproate, increase the dose and explain her risk of teratogenicity",
                "Stop Valproate and start her on Levetiracetam",
                "Stop Valproate and start her on Phenytoin",
                "Put her on polytherapy as one drug might not be effective"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Stop Valproate and start her on Levetiracetam.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.52)"
        },
        {
            "id": "cms26-p2-053",
            "subject": "Obstetrics & Gynaecology",
            "text": "The next step to follow for a mother with Rh-negative pregnancy and antibody titre above critical level (husband Rh- positive) is",
            "options": [
                "umbilical artery Doppler",
                "cordocentesis",
                "MCA PSV",
                "amniocentesis"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — MCA PSV.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.53)"
        },
        {
            "id": "cms26-p2-054",
            "subject": "Obstetrics & Gynaecology",
            "text": "Match List-I with List-II and select the correct answer using the code given below the Lists: List-I List-II (Description of condition (Type of in early pregnancy) abortion) A. Increased vaginal 1. Missed bleeding, aggravated abortion pelvic pain and dilated internal os B. Brownish vaginal 2. Inevitable discharge and absent abortion fetal heart on ultra- sound at 11 weeks C. Decreased or absent 3. Threatened vaginal bleeding, abortion pelvic pain subsides and closed internal os D. Slight bleeding per 4. Complete vaginum, mild pelvic abortion pain and fetal heart present on ultra- sound Code :",
            "options": [
                "A B C D 2 4 1 3",
                "A B C D 3 1 4 2",
                "B C D 2 1 4 3",
                "B C D 4 1 2"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — B C D 2 1 4 3.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.54)"
        },
        {
            "id": "cms26-p2-055",
            "subject": "Obstetrics & Gynaecology",
            "text": "Early-onset fetal growth restriction is diagnosed before",
            "options": [
                "28 weeks of gestation",
                "30 weeks of gestation",
                "32 weeks of gestation",
                "34 weeks of gestation"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 32 weeks of gestation.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.55)"
        },
        {
            "id": "cms26-p2-056",
            "subject": "Obstetrics & Gynaecology",
            "text": "Consider the following statements regarding vaginal epithelium in adult female : 1. From puberty till menopause, the vaginal epithelium is devoid of any gland. 2. The basal epithelial layer contains glycogen. 3. Intermediate and superficial cells become continuous with those covering vaginal portion of cervix. 4. Unlike skin, it does not contain hair follicle. Which of the statements given above are correct?",
            "options": [
                "1, 3 and 4",
                "1, 2 and 4",
                "2, 3 and 4",
                "1, 2 and 3"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 1, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.56)"
        },
        {
            "id": "cms26-p2-057",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which one of the following statements is true regarding neurovascular anatomy of the uterus?",
            "options": [
                "The uterine artery arises from the anterior division of the external iliac artery.",
                "The uterine artery crosses the ureter 3•5 cm lateral to the internal os.",
                "The venous channels of the uterus drain into the internal iliac veins.",
                "The somatic distribution of the uterine pain is the area of the abdomen supplied by Ts and T6"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — The venous channels of the uterus drain into the internal iliac veins..",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.57)"
        },
        {
            "id": "cms26-p2-058",
            "subject": "Obstetrics & Gynaecology",
            "text": "Match List-I with List-II and select the correct answer using the code given below the Lists : List-I List-Il (Embryonic (Developed organ/ structure structure in female) A. Gubernaculum 1. Clitoris B. Genital tubercle 2. Uterus C. Mesonephric duct 3. Round ligament D. Paramesonephric 4. Urethra duct Code :",
            "options": [
                "A B",
                "A B 2 4",
                "A B C",
                "A B C D 3 4 2"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — A B C.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.58)"
        },
        {
            "id": "cms26-p2-059",
            "subject": "Obstetrics & Gynaecology",
            "text": "When does the secondary oocyte complete the second meiotic division?",
            "options": [
                "Just before ovulation",
                "Just after ovulation",
                "Just before fertilization",
                "Just after fertilization"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Just after fertilization.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.59)"
        },
        {
            "id": "cms26-p2-060",
            "subject": "Obstetrics & Gynaecology",
            "text": "The growth and differentiation of primordial follicles is under the control of which hormone?",
            "options": [
                "LH",
                "FSH",
                "Growth hormone",
                "Progesterone"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — FSH.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.60)"
        },
        {
            "id": "cms26-p2-061",
            "subject": "Obstetrics & Gynaecology",
            "text": "Consider the following statements with respect to endometrial cycle : 1. The basal zone is uninfluenced by any hormone. 2. Saw-toothed glandular epithelium is seen in secretory phase. 3. Stratum compactum contains mainly the glands and less stroma. 4. Pseudostratification is seen in proliferative phase of menstrual cycle. Which of the statements given above are correct?",
            "options": [
                "1, 3 and 4",
                "1, 2 and 4",
                "2, 3 and 4",
                "1, 2 and 3"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1, 2 and 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.61)"
        },
        {
            "id": "cms26-p2-062",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which one of the following statements explains self-priming of gonadotrophs?",
            "options": [
                "Lower GnRH pulse frequencies favour FSH secretion and higher frequencies favour LH secretion.",
                "Lower GnRH pulse frequencies favour LH secretion and higher frequencies favour FSH secretion.",
                "Lower GnRH pulse frequencies favour LH as well as FSH secretion.",
                "Higher GnRH pulse frequencies favour LH as well as FSH secretion."
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Lower GnRH pulse frequencies favour FSH secretion and higher frequencies favour LH secretion..",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.62)"
        },
        {
            "id": "cms26-p2-063",
            "subject": "Obstetrics & Gynaecology",
            "text": "Consider the following diagnostic criteria for acute pelvic inflammatory disease (PID) : 1. Lower abdominal tenderness 2. Oral temperature >38 °C 3. Adnexal tenderness 4. Cervical motion tenderness Which of the above are included in the minimum criteria for diagnosis of PID?",
            "options": [
                "1, 2 and 3",
                "1, 2 and 4",
                "1, 3 and 4",
                "2, 3 and 4"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 1, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.63)"
        },
        {
            "id": "cms26-p2-064",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which one of the following statements is true regarding genital tuberculosis?",
            "options": [
                "The most common site of affection is ovary.",
                "Abdominal ostium is closed in tobacco pouch appearance.",
                "The most common mode of spread from primary to genital organs is haematogenous.",
                "Genital tuberculosis occurs in 1-2% of patients who had pulmonary tuberculosis adolescence."
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — The most common mode of spread from primary to genital organs is haematogenous..",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.64)"
        },
        {
            "id": "cms26-p2-065",
            "subject": "Obstetrics & Gynaecology",
            "text": "The drug of choice for treatment of chlamydial cervicitis is",
            "options": [
                "Metronidazole",
                "Ampicillin",
                "Azithromycin",
                "Secnidazole"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Azithromycin.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.65)"
        },
        {
            "id": "cms26-p2-066",
            "subject": "Obstetrics & Gynaecology",
            "text": "Kit 6 used in syndromic management of STI/RTI includes which one of the following drug combinations?",
            "options": [
                "Cefixime, Metronidazole Doxycycline",
                "Cefixime, Secnidazole Fluconazole",
                "Metronidazole, Doxycycline and Fluconazole",
                "Acyclovir, Doxycycline Metronidazole"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Cefixime, Metronidazole Doxycycline.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.66)"
        },
        {
            "id": "cms26-p2-067",
            "subject": "Obstetrics & Gynaecology",
            "text": "The most common site for vulvar carcinoma is",
            "options": [
                "labia minora",
                "labia majora",
                "clitoris",
                "mons pubis"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — labia majora.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.67)"
        },
        {
            "id": "cms26-p2-068",
            "subject": "Obstetrics & Gynaecology",
            "text": "Point A in radiotherapy in carcinoma cervix marks the site for which of the following structures?",
            "options": [
                "Obturator nodes",
                "Inguinal nodes",
                "Crossing of ureter by uterine artery",
                "Crossing of ureter by descending cervical artery"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Crossing of ureter by uterine artery.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.68)"
        },
        {
            "id": "cms26-p2-069",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which one of the following states the diagnostic criteria for postmolar gestational trophoblastic neoplasia?",
            "options": [
                "A rise of hCG levels of more than 10% for >3 values over 2 weeks' time",
                "A rise of hCG levels of more than 5% for >4 values over 2 weeks' time",
                "A rise of hCG levels of more than 15% for >3 values over 2 weeks' time",
                "A rise of hCG levels of more than 10% for >3 values over 4 weeks' time"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — A rise of hCG levels of more than 10% for >3 values over 2 weeks' time.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.69)"
        },
        {
            "id": "cms26-p2-070",
            "subject": "Obstetrics & Gynaecology",
            "text": "Consider the following regarding the steps in Fothergill repair surgery for uterine prolapse : 1. Plication of Mackenrodt's ligament in front of the cervix 2. Shortening of uterosacral ligaments 3. Plication of Mackenrodt's ligament behind the cervix 4. Amputation of the cervix Which of the above steps form a part of steps in Fothergill repair surgery for uterine prolapse?",
            "options": [
                "2 and 4",
                "1 and 4",
                "1 and 2",
                "3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 1 and 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.70)"
        },
        {
            "id": "cms26-p2-071",
            "subject": "Obstetrics & Gynaecology",
            "text": "Consider the following surgical methods: 1. Haultain's method 2. Gilliam's operation 3. Spinelli's operation 4. Cutting anterior cervical ring Which of the methods given above may be used for surgical management of chronic uterine inversion?",
            "options": [
                "1, 2 and 3",
                "2, 3 and 4",
                "1, 3 and 4",
                "1, 2 and 4"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 1, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.71)"
        },
        {
            "id": "cms26-p2-072",
            "subject": "Obstetrics & Gynaecology",
            "text": "If 100 couples have used a method for a period of 2 years and have resulted resulted in 10 pregnancies, what will be the effectiveness of the method used?",
            "options": [
                "High",
                "Moderate",
                "Low",
                "Cannot be commented"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — High.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.72)"
        },
        {
            "id": "cms26-p2-073",
            "subject": "Obstetrics & Gynaecology",
            "text": "In postpartum period, the intrauterine device may be inserted in the woman",
            "options": [
                "up to 72 hours of delivery",
                "up to 48 hours of delivery",
                "up to 36 hours of delivery",
                "up to 24 hours of delivery"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — up to 48 hours of delivery.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.73)"
        },
        {
            "id": "cms26-p2-074",
            "subject": "Obstetrics & Gynaecology",
            "text": "Consider the following conditions in a woman of reproductive age group : 1. Diabetes with retinopathy 2. Age 36 years, non-smoker 3. Liver adenoma 4. History of stroke Which of the above are absolute contraindications for using combined oral contraceptive pills?",
            "options": [
                "1, 2 and 3",
                "2, 3 and 4",
                "1, 3 and 4",
                "1, 2 and 4"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 1, 3 and 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.74)"
        },
        {
            "id": "cms26-p2-075",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which of the following statements regarding progesterone-only pills are correct? 1. They contain high-dose proges- terone as there is no estrogen component. 2. They do not have 'on and off\" regimen. 3. They can be used with hepatic enzyme inducing drugs. 4. The failure rate is 0-3 to 2 per hundred women-years of use. Select the answer using the code given below.",
            "options": [
                "2 and 4",
                "1 and 3",
                "1 and 4",
                "2 and 3"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 2 and 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.75)"
        },
        {
            "id": "cms26-p2-076",
            "subject": "Obstetrics & Gynaecology",
            "text": "After undergoing vasectomy, how many ejaculations and months are required for a man to become sterile?",
            "options": [
                "30 ejaculations and 2 months",
                "20 ejaculations and 2 months",
                "20 ejaculations and 3 months",
                "30 ejaculations and 3 months"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 20 ejaculations and 3 months.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.76)"
        },
        {
            "id": "cms26-p2-077",
            "subject": "Obstetrics & Gynaecology",
            "text": "Which of the following statements regarding lactational amenorrhea method are correct? 1. It is equally effective in amenorrheic as well menstruating woman if the woman is exclusively breastfeeding. 2. The risk of pregnancy in amenorrheic woman who is exclusively breastfeeding is less than 2% in the first 6 months. 3. It requires exclusive breastfeeding for 6 months. 4. The failure rate for exclusively breastfeeding and menstruating women is 15-20%. Select the answer using the code given below.",
            "options": [
                "2 and 4",
                "2 and 3",
                "3 and 4",
                "1 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.77)"
        },
        {
            "id": "cms26-p2-078",
            "subject": "Obstetrics & Gynaecology",
            "text": "Laparoscopic tubal sterilization can be done after",
            "options": [
                "48 hours of delivery",
                "7 days of delivery",
                "2 weeks of delivery",
                "6 weeks of delivery"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 6 weeks of delivery.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.78)"
        },
        {
            "id": "cms26-p2-079",
            "subject": "Obstetrics & Gynaecology",
            "text": "According to the Medical Termination of Pregnancy (Amendment) Act, 2021, MTP for pregnancy between 20 to 24 weeks needs opinion of",
            "options": [
                "one registered medical practitioner",
                "two registered medical practitioners",
                "one registered medical practitioner and court order",
                "two registered medical practitioners and court order"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — two registered medical practitioners.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.79)"
        },
        {
            "id": "cms26-p2-080",
            "subject": "Obstetrics & Gynaecology",
            "text": "The combi-pack approved by the DGHS for medical method of MTP in the first trimester comprises of which one of the following combinations?",
            "options": [
                "200 mg Mifepristone and 800 ug Misoprostol",
                "100 mg Mifepristone and 400 ug Misoprostol",
                "400 mg Mifepristone and 800 ug Misoprostol",
                "200 mg Mifepristone and 600 ug Misoprostol"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 200 mg Mifepristone and 800 ug Misoprostol.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.80)"
        },
        {
            "id": "cms26-p2-081",
            "subject": "Preventive & Social Medicine",
            "text": "In the history of public health, as a part of modern medicine, the following four distinct phases can be demarcated : 1. 'Health for All' phase 2. Health promotional phase 3. Disease control phase 4. Social engineering phase Which one of the following represents the correct sequence of the phases in chronological order (from the oldest to the newest)?",
            "options": [
                "1 → 3 → 2 → 4",
                "2→4 → 1→3",
                "3 → 2→4→1",
                "4 → 1 → 3 → 2"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 3 → 2→4→1.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.81)"
        },
        {
            "id": "cms26-p2-082",
            "subject": "Preventive & Social Medicine",
            "text": "A person meets with an accident and as a result of which, the person loses his/her right arm, because of which the person is not able to drive the car to reach his/her office, and has to hire a driver for the same. The given condition of the person is most appropriately classified as",
            "options": [
                "impairment",
                "disease",
                "disability",
                "handicap"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — disability.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.82)"
        },
        {
            "id": "cms26-p2-083",
            "subject": "Preventive & Social Medicine",
            "text": "As per the 2030 Agenda for Sustainable Development', the target '34' refers to which one of the following?",
            "options": [
                "By 2030, reduce the global maternal mortality ratio to less than 70 per 100000 live births",
                "By 2020, halve the number of global deaths and injuries from road traffic accidents",
                "By 2030, reduce by 1/3rd premature mortality from non- communicable diseases through prevention and treatment, and promote mental health and well-being",
                "Strengthen the prevention and treatment of substance abuse, including narcotic drug abuse and harmful use of alcohol"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — By 2030, reduce by 1/3rd premature mortality from non- communicable diseases through prevention and treatment, and promote mental health and well-being.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.83)"
        },
        {
            "id": "cms26-p2-084",
            "subject": "Preventive & Social Medicine",
            "text": "In a given set of conditions, a screening test has 90% sensitivity and 90% specificity for screening a particular disease. The prevalence of the disease at the given time in that population is 10%. Which one of the following statements regarding positive predictive value of the test is correct?",
            "options": [
                "The positive predictive value is 90%.",
                "The positive predictive value is 70%.",
                "The positive predictive value is 60%.",
                "The positive predictive value is 50%."
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — The positive predictive value is 50%..",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.84)"
        },
        {
            "id": "cms26-p2-085",
            "subject": "Preventive & Social Medicine",
            "text": "In a historical study, the death rate among heavy smokers was 224 per 1 lakh person-years while among non-smokers was 10 per 1 lakh person-years. The death rate in the general population was 74 per 1 lakh person-years. Which one among the following best represents the attributable risk of smoking for mortality in the given scenario?",
            "options": [
                "22•4%",
                "86￾5%",
                "95￾5%",
                "67•0%"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 95￾5%.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.85)"
        },
        {
            "id": "cms26-p2-086",
            "subject": "Preventive & Social Medicine",
            "text": "The changes that the malarial parasite undergoes in the mosquito represent which one of the following types of biological transmission?",
            "options": [
                "Propagative",
                "Developmental",
                "Cyclopropagative",
                "Cyclodevelopmental"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Cyclopropagative.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.86)"
        },
        {
            "id": "cms26-p2-087",
            "subject": "Preventive & Social Medicine",
            "text": "In a given population of 10000, there were 30 cases of diabetes already present on 01/01/2025 and in the year 2025, 400 more cases developed diabetes. But 10 cases of diabetes died in the year 2025, i.e., before 31/12/2025. Which one of the following statements is correct regarding the disease situation?",
            "options": [
                "The incidence of diabetes in the population is 42/1000.",
                "The point prevalence of diabetes on 31/12/2025 was 43/1000.",
                "The period prevalence of diabetes in 2025 was 43/1000.",
                "The prevalence of diabetes in 2025 was 44/1000."
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — The period prevalence of diabetes in 2025 was 43/1000..",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.87)"
        },
        {
            "id": "cms26-p2-088",
            "subject": "Preventive & Social Medicine",
            "text": "The parameter which provides an estimate of the amount by which the disease under study can be reduced in a population, if the suspected factor is eliminated from that population, is called",
            "options": [
                "relative risk",
                "attributable risk",
                "population attributable risk",
                "risk difference"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — population attributable risk.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.88)"
        },
        {
            "id": "cms26-p2-089",
            "subject": "Preventive & Social Medicine",
            "text": "Which of the following correctly represent late expanding', i.e., the third stage in the 'demographic cycle\"?",
            "options": [
                "High birthrates and high death rates",
                "Decline in death rates and decline in birthrates",
                "Decline in death rates and rising birthrates",
                "Low death rates and low birthrates"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Decline in death rates and decline in birthrates.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.89)"
        },
        {
            "id": "cms26-p2-090",
            "subject": "Preventive & Social Medicine",
            "text": "Which one of the following statements regarding sample registration system is not correct?",
            "options": [
                "It is a dual record system.",
                "It is a continuous enumeration by local enumerators and an independent survey every year by an investigator-supervisor.",
                "It covers the entire country.",
                "It has facilitated more reliable estimates of births and deaths even at State level."
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — It is a continuous enumeration by local enumerators and an independent survey every year by an investigator-supervisor..",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.90)"
        },
        {
            "id": "cms26-p2-091",
            "subject": "Preventive & Social Medicine",
            "text": "Which one of the following fertility- related statistics most appropriately gives the approximate magnitude of 'completed family size?",
            "options": [
                "Total Fertility Rate (TFR)",
                "Total Marital Fertility Rate (TMFR)",
                "Net Reproduction Rate (NRR)",
                "Age-Specific Fertility Rate (ASFR)"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Total Fertility Rate (TFR).",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.91)"
        },
        {
            "id": "cms26-p2-092",
            "subject": "Preventive & Social Medicine",
            "text": "A person had undergone the serology for suspected hepatitis B infection. His/ Her serology shows the presence of HBs antigen and also IgG anti-HBc along with the presence of anti-HBe, while HBe antigen is negative. Which one of the following diagnoses is the correct interpretation of the serology results?",
            "options": [
                "Active hepatitis B infection",
                "Chronic hepatitis B infection with active viral replication",
                "Chronic hepatitis B infection with low viral replication",
                "Recovery/Vaccination from hepatitis B"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Chronic hepatitis B infection with low viral replication.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.92)"
        },
        {
            "id": "cms26-p2-093",
            "subject": "Preventive & Social Medicine",
            "text": "Inoculation rate', an important vector index for malaria survey, is correctly defined as",
            "options": [
                "average number of anopheline bites per day per person",
                "percentage of female anophelines with sporozoites in their salivary glands",
                "man-biting rate multiplied by infective sporozoite rate",
                "proportion of freshly fed female anophelines whose stomach contains human blood"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — man-biting rate multiplied by infective sporozoite rate.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.93)"
        },
        {
            "id": "cms26-p2-094",
            "subject": "Preventive & Social Medicine",
            "text": "A doctor receives a telephonic call from the mother of an 8-year-old boy, who informs that the boy has just been bitten by a monkey. The child was playing with his friends when a group of monkeys appeared nearby. Some of the children shouted and threw sticks and stones at the monkeys, who became angry and aggressive. One of the monkeys bit the lady's son in the forearm and blood is visible over the wound. The nearest health facility is 3 kilometers away. Consider the following statements regarding how the doctor should respond : 1. Advise the mother to rush with the child to the health facility without waiting for anything. 2. Advise the mother to first thoroughly wash the wound with plenty of soap and running water for at least 15 minutes, and then seek treatment. 3. Advise the mother that the animal bite is category I and risk is very low, as the bite was provoked. 4. Advise the mother to seek treatment for the boy's wound but the boy requires no treatment or prophylaxis for rabies as it is a monkey bite. Which of the statements given above is / are correct?",
            "options": [
                "1 only",
                "2 only",
                "1 and 3",
                "2 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 2 only.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.94)"
        },
        {
            "id": "cms26-p2-095",
            "subject": "Preventive & Social Medicine",
            "text": "Horrocks' apparatus was used to find out the dose of bleaching powder required to disinfect the water in a well. The 3rd cup in the Horrocks' apparatus showed the distinct blue colour. How much bleaching powder (good quality) will be required to disinfect the well, for every 455 liters of water?*",
            "options": [
                "3 grams",
                "12 grams",
                "9 grams",
                "6 grams"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 6 grams.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.95)"
        },
        {
            "id": "cms26-p2-096",
            "subject": "Preventive & Social Medicine",
            "text": "To be effective, the size of the openings in the mosquito net should not exceed",
            "options": [
                "0•0475 inch in diameter",
                "0:00475 inch in diameter",
                "0•0475 centimeter in diameter",
                "0:00475 centimeter in diameter"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — 0•0475 inch in diameter.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.96)"
        },
        {
            "id": "cms26-p2-097",
            "subject": "Preventive & Social Medicine",
            "text": "As per the WHO expert group, the cutoff point of haemoglobin in venous blood for the diagnosis of anaemia in adult males is",
            "options": [
                "12 g/dL",
                "13 g/dL",
                "11 g/dL",
                "14 g/dL"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 13 g/dL.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.97)"
        },
        {
            "id": "cms26-p2-098",
            "subject": "Preventive & Social Medicine",
            "text": "A 12-year-old boy presented to a health centre in Telangana along with his parents, with complaints of recurrent diarrhea, and skin changes on areas of the body exposed to sunlight. There is a history of progressive disorientation and increasing irritability. The child and his tamily ate sorghum cereal, there was very little consumption of milk and no consumption of foods of animal origin like meat, though the family is not strictly vegetarian by food habit. Consider the following plans of action: 1. Absolute avoidance of milk in the child's diet 2. Encouraging shift of cereal consumption from sorghum to maize 3. Encouraging consumption of meat in the child's diet, if the family can afford 4. Supplementation with nicotinic acid or nicotinamide Which of the plans of action given above are correct?",
            "options": [
                "1 and 2 only",
                "3 and 4 only",
                "1, 2 and 3",
                "2, 3 and 4"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 3 and 4 only.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.98)"
        },
        {
            "id": "cms26-p2-099",
            "subject": "Preventive & Social Medicine",
            "text": "As per the National Blindness and Visual Impairment Survey India (2015-2019), which one of the following is the most common cause of blindness in India?",
            "options": [
                "Glaucoma",
                "Diabetic retinopathy",
                "Refractive error (untreated)",
                "Cataract (untreated)"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Cataract (untreated).",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.99)"
        },
        {
            "id": "cms26-p2-100",
            "subject": "Preventive & Social Medicine",
            "text": "Which one of the following most appropriately describes the tracking' phenomenon of blood pressure?",
            "options": [
                "Continuous monitoring of blood pressure on any individual to keep a track of blood pressure for early diagnosis of hypertension",
                "Persistence of rank order of blood pressure in individuals as they grow older",
                "Keeping a track of the prevalence of hypertension in a community",
                "Tracking of twins for change in blood pressure to see the effect of genetic makeup"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Persistence of rank order of blood pressure in individuals as they grow older.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.100)"
        },
        {
            "id": "cms26-p2-101",
            "subject": "Preventive & Social Medicine",
            "text": "An adult is weighing 80 kg and having a height of 16 meters. Under which category does the individual fall as per the WHO classification of BMI?",
            "options": [
                "Normal",
                "Pre-obese",
                "Obese class I",
                "Obese class II"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — Obese class I.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.101)"
        },
        {
            "id": "cms26-p2-102",
            "subject": "Preventive & Social Medicine",
            "text": "A 42-year-old male industrial worker presented to a health centre with complaints of diminished working capacity, and debilitating respiratory complaints including chronic irritant cough, severe dyspnea on exertion and occasional pain in chest. He gave an in the lung fields. High resolution radiographic imaging showed dense nodular fibrosis in the lungs. Which one of the following is the most likely diagnosis for this case?",
            "options": [
                "Asbestosis",
                "Bagassosis",
                "Byssinosis",
                "Silicosis"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Silicosis.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.102)"
        },
        {
            "id": "cms26-p2-103",
            "subject": "Preventive & Social Medicine",
            "text": "Leukemia', as an occupational cancer, is most commonly related to the exposure to which one of the following industrial chemicals?",
            "options": [
                "Mineral oil",
                "Auramine",
                "Beta-naphthylamine",
                "Benzol"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Benzol.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.103)"
        },
        {
            "id": "cms26-p2-104",
            "subject": "Preventive & Social Medicine",
            "text": "Which one of the following statements regarding sex chromosomes in the human body is correct?",
            "options": [
                "Chromosome X is included in Group C of the autosomal chromosomes.",
                "Chromosome Y is included in Group E of the autosomal chromosomes.",
                "Chromosome X is included in Group G of the autosomal chromosomes.",
                "Chromosome Y is included in Group F of the autosomal chromosomes."
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Chromosome X is included in Group C of the autosomal chromosomes..",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.104)"
        },
        {
            "id": "cms26-p2-105",
            "subject": "Preventive & Social Medicine",
            "text": "Consider the following organizations of importance in the history of international health : 1. The Health Organization of the League of Nations 2. The Pan American Sanitary Bureau 3. The United Nations Relief and Rehabilitation Administration 4. The World Health Organization Which one of the following represents the correct chronological order (from the oldest to the newest) of the establishment of these organizations?",
            "options": [
                "1 → 2 → 4 → 3",
                "1→3 → 4→2",
                "2→4 → 1→3",
                "2→1→3 → 4"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — 2→1→3 → 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.105)"
        },
        {
            "id": "cms26-p2-106",
            "subject": "Preventive & Social Medicine",
            "text": "Which one among the following terms best fits the description \"the entire gamut of preventive, therapeutic and rehabilitative services for the protection of society from antisocial, criminal or deviant conduct of man\"?",
            "options": [
                "Social delinquency",
                "Social defence",
                "Social pathology",
                "Social survey"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Social defence.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.106)"
        },
        {
            "id": "cms26-p2-107",
            "subject": "Preventive & Social Medicine",
            "text": "A 10-week-old infant was taken to a primary health centre by his/her mother for vaccination. The infant has taken all the doses as per the recommended schedule of immunization at 6 weeks. The infant was prescribed Pentavalent and Rotavirus vaccine. After 3 days of getting the vaccine, the mother reported to the PHC that the infant has suffered an episode of epilepsy. On enquiring, it was found that the infant had a history of two epileptic episodes in the week prior to immunization, i.e., the 9th week. Considering the scenario, which one of the following statements is correct regarding this adverse event following immunization (AEFI)?",
            "options": [
                "It is vaccine product related AEFI.",
                "It is immunization error related AEFI.",
                "It is immunization stress related AEFI.",
                "It is a coincidental event."
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — It is immunization error related AEFI..",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.107)"
        },
        {
            "id": "cms26-p2-108",
            "subject": "Preventive & Social Medicine",
            "text": "All of the following correctly represent the basic criteria for identifying 'at risk' infants, except",
            "options": [
                "birth order 3 and above",
                "twins",
                "failure to gain weight during three successive months",
                "on artificial feeding"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — birth order 3 and above.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.108)"
        },
        {
            "id": "cms26-p2-109",
            "subject": "Preventive & Social Medicine",
            "text": "Which of the following drugs have been as part of mass administration (MDA) for elimination of lymphatic filariasis in some or more districts of India? 1. Albendazole 2. Diethylcarbamazine 3. Ivermectin 4. Metronidazole Select the correct answer using the code given below.",
            "options": [
                "2 and 3 only",
                "1 and 4 only",
                "1, 2 and 3",
                "1, 2 and 4"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 1, 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.109)"
        },
        {
            "id": "cms26-p2-110",
            "subject": "Preventive & Social Medicine",
            "text": "As per the National Framework for Malaria Elimination India (2016-2030), which one of the following has to be achieved by the year 2027?",
            "options": [
                "The entire country to have less than 1 case due to malaria per 1000 population at risk",
                "The entire country to have less than 1 indigenous case of malaria per 1000 population at risk and less than 1 death due to malaria per 10000 population at risk",
                "The entire country to have indigenous case of malaria and less than 1 death due to malaria per 100000 population at risk",
                "The entire country to have no indigenous case of malaria and no deaths due to malaria"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — The entire country to have no indigenous case of malaria and no deaths due to malaria.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.110)"
        },
        {
            "id": "cms26-p2-111",
            "subject": "Preventive & Social Medicine",
            "text": "As per the Jal Jeevan Mission (JJM), the goal is to provide every rural household with a functional household connection that delivers at least how many liters of tap water per capita per day (Ipcd)?",
            "options": [
                "35",
                "55",
                "75",
                "105"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — 55.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.111)"
        },
        {
            "id": "cms26-p2-112",
            "subject": "Preventive & Social Medicine",
            "text": "Which of the following vaccines are live vaccines?",
            "options": [
                "BCG, Measles, Injectable Polio Vaccine (IPV)",
                "Measles, OPV, Yellow Fever (17D) Vaccine",
                "BCG, IPV, Plague Vaccine",
                "OPV, Hib Vaccine, HBV"
            ],
            "correct_option": 1,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (b) — Measles, OPV, Yellow Fever (17D) Vaccine.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.112)"
        },
        {
            "id": "cms26-p2-113",
            "subject": "Preventive & Social Medicine",
            "text": "Directions : Read the following case scenario and answer the two items that follow the case scenario. Your answers to these items should be based on the case scenario only. A 6-week-old infant has a history of fever for 2 days, and according to the mother, is not feeding well, taking 2-3 breastfeeds in a day. The infant has diarrhea for the last 2 days and has sunken eyes. The pus is draining from the umbilicus and the infant has a respiratory rate of 55 breaths per minute. 113. Which one of the following is correct regarding the classification of the infant as per the IMNCI guidelines?",
            "options": [
                "Very severe disease",
                "Local bacterial infection",
                "No dehydration",
                "Severe dehydration"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — Very severe disease.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.113)"
        },
        {
            "id": "cms26-p2-114",
            "subject": "Preventive & Social Medicine",
            "text": "What is/are the most appropriate treatments) for the infant? 1. Give 1st dose of intramuscular antibiotics. 2. Refer the child urgently to hospital and advise mother to continue breastfeeding. 3. Advise mother to give frequent sips of ORS on the way. 4. Teach mother to treat local infection and send home with advice for a follow-up after 2 days. Select the correct answer using the code given below.",
            "options": [
                "1 and 2 only",
                "2 and 3 only",
                "1, 2 and 3",
                "4"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 1, 2 and 3.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.114)"
        },
        {
            "id": "cms26-p2-115",
            "subject": "Preventive & Social Medicine",
            "text": "Directions : Read the following case scenario and answer the five items that follow the case scenario. Your answers to these items should be based on the case scenario only. Mrs. M is a poor, migrant worker who has recently moved into a village along with her husband to work in the local brick kiln. They both will now be staying in this village for a while. The ASHA of that particular village visits her and comes to know that she has missed her last period. The last menstrual period (LMP) was on 6th January, while the ASHA visited her on 4th March of the same year. The lady has never delivered a child or had an abortion earlier. The ASHA talks to her and finds out that her age is 28 years, and measures that her height is 144 cm and weight is 52 kg. A blood test was performed and her haemoglobin was found to be 11•6 g/dL. 115. Which one among the following test kits available under the National Health Programme can the ASHA use for the confirmation of pregnancy in this case?",
            "options": [
                "Abha kit",
                "Lakshya kit",
                "Nikshay kit",
                "Nischay kit"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — Nischay kit.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.115)"
        },
        {
            "id": "cms26-p2-116",
            "subject": "Preventive & Social Medicine",
            "text": "Once the confirmation of the pregnancy is done, consider the following statements regarding the registration of pregnancy : 1. It is to be done as soon as possible, and within 12 weeks. 2. It is to be done as soon as possible, once 12 weeks are complete. 3. It is the primary responsibility of the ASHA. 4. It is the primary responsibility of the ANM. Which of the statements given above are correct?",
            "options": [
                "1 and 3",
                "2 and 4",
                "1 and 4",
                "2 and 3"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 1 and 4.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.116)"
        },
        {
            "id": "cms26-p2-117",
            "subject": "Preventive & Social Medicine",
            "text": "Assuming that a pregnancy was confirmed, the ASHA informed Mrs. M that she should take iron and folic acid (IFA) supplementation for a minimum of X days during her pregnancy period, under the Government's Anaemia Mukt Bharat Programme. Which one among the following best represents the X?",
            "options": [
                "60",
                "100",
                "180",
                "240"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 180.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.117)"
        },
        {
            "id": "cms26-p2-118",
            "subject": "Preventive & Social Medicine",
            "text": "From the data given in the case scenario, consider if the lady's pregnancy would fall under a high-risk' pregnancy on account of 1. her age 2. her height and parity 3. her haemoglobin level Mrs. M's pregnancy qualifies as a 'high-risk' pregnancy under which of the above parameters?",
            "options": [
                "1",
                "2",
                "3",
                "None of the above"
            ],
            "correct_option": 3,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (d) — None of the above.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.118)"
        },
        {
            "id": "cms26-p2-119",
            "subject": "Preventive & Social Medicine",
            "text": "Consider the following advices to be given by the ASHA to Mrs. M (assuming pregnancy has been confirmed) regarding personal hygiene measures : 1. Minimum 12 hours sleep at a stretch at night 2. Avoid resting immediately after mid-day meals 3. Avoid intake of extra fluids to avoid constipation 4. Avoid taking purgatives like castor oil to relieve constipation How many of the four advices listed above are correct?",
            "options": [
                "One",
                "Two",
                "Three",
                "Four"
            ],
            "correct_option": 0,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (a) — One.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.119)"
        },
        {
            "id": "cms26-p2-120",
            "subject": "Preventive & Social Medicine",
            "text": "Although different triage systems have been used as a part of disaster response, classification uses the following internationally accepted four-colour code system : 1. Black 2. Green 3. Red 4. Yellow Which one among the following correctly represents the descending order (from the highest to the lowest) of priority for medical care and transportation to health centres?",
            "options": [
                "1 → 3 → 4→2",
                "2→4→1→3",
                "3→4→2 → 1",
                "3 → 2→4 → 1 SPACE FOR ROUGH WORK SPACE FOR ROUGH WORK SPACE FOR ROUGH WORK SPACE FOR ROUGH WORK * * * 32 26BS-115968"
            ],
            "correct_option": 2,
            "explanation": "Official UPSC CMS 2026 Series A Provisional Answer Key: Option (c) — 3→4→2 → 1.",
            "citation": "UPSC CMS 2026 Paper-II (NTDC-T-GSPO Series-A Q.120)"
        }
    ]
}
