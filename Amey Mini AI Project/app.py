"""
AI Citizen Services Assistant — BCA Mini Project
A rule-based assistant to help users discover Indian public service portals,
basic document checklists, and scheme information. Verify details on official sites.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="AI Citizen Services Assistant", page_icon="🇮🇳", layout="wide")

SERVICES = [
    {
        "name": "Aadhaar Services",
        "category": "Identity & Documents",
        "description": "Aadhaar updates, enrolment information, status and related services.",
        "keywords": ["aadhaar", "aadhar", "uidai", "identity", "address update", "mobile update"],
        "documents": ["Aadhaar number or enrolment ID, where applicable", "Supporting identity/address document as requested by UIDAI"],
        "url": "https://uidai.gov.in/",
        "note": "Requirements and available online services vary by request."
    },
    {
        "name": "PAN Services",
        "category": "Identity & Documents",
        "description": "PAN application and related income-tax services.",
        "keywords": ["pan", "permanent account number", "income tax", "tax id"],
        "documents": ["Identity proof", "Address proof", "Date-of-birth proof, as required"],
        "url": "https://www.incometax.gov.in/",
        "note": "Use the official Income Tax portal to verify the correct PAN service and process."
    },
    {
        "name": "Passport Services",
        "category": "Identity & Documents",
        "description": "Passport application, appointment and application-status information.",
        "keywords": ["passport", "travel document", "passport status", "appointment"],
        "documents": ["Proof of address", "Proof of date of birth", "Other documents specified for your application category"],
        "url": "https://www.passportindia.gov.in/",
        "note": "The exact document list depends on the application category and personal circumstances."
    },
    {
        "name": "DigiLocker",
        "category": "Digital Services",
        "description": "Access and manage eligible digital documents and certificates.",
        "keywords": ["digilocker", "digital documents", "certificates", "marksheet", "documents"],
        "documents": ["Mobile number or other account details requested during sign-in"],
        "url": "https://www.digilocker.gov.in/",
        "note": "Only documents available from participating issuers can be fetched."
    },
    {
        "name": "Scholarship Portal",
        "category": "Education",
        "description": "Find information about scholarships and application opportunities.",
        "keywords": ["scholarship", "student", "education grant", "national scholarship", "fees"],
        "documents": ["Student and course details", "Income/caste/category documents if applicable", "Bank details and academic records if requested"],
        "url": "https://scholarships.gov.in/",
        "note": "Eligibility, deadlines and required documents depend on the specific scholarship."
    },
    {
        "name": "MyScheme",
        "category": "Schemes & Benefits",
        "description": "Discover government schemes and review their eligibility information.",
        "keywords": ["scheme", "government benefit", "eligibility", "yojana", "benefits", "subsidy"],
        "documents": ["Documents listed on the official page of the scheme you select"],
        "url": "https://www.myscheme.gov.in/",
        "note": "The assistant does not decide eligibility. Confirm all criteria on the official scheme page."
    },
    {
        "name": "PM-KISAN",
        "category": "Farmers",
        "description": "Official information and services for the PM-KISAN scheme.",
        "keywords": ["farmer", "farmers", "pm kisan", "pm-kisan", "agriculture", "kisan"],
        "documents": ["Land and identity details as required by the official process", "Bank details if requested"],
        "url": "https://pmkisan.gov.in/",
        "note": "Scheme eligibility and payment status should be checked through official channels."
    },
    {
        "name": "Ayushman Bharat PM-JAY",
        "category": "Health",
        "description": "Official information about PM-JAY health coverage and beneficiary services.",
        "keywords": ["health", "hospital", "ayushman", "pmjay", "pm-jay", "medical benefit"],
        "documents": ["Details needed for beneficiary search or verification as shown on the official portal"],
        "url": "https://pmjay.gov.in/",
        "note": "Coverage and beneficiary status must be verified through official sources."
    },
    {
        "name": "Voter Services",
        "category": "Civic Services",
        "description": "Voter registration and related Electoral Commission services.",
        "keywords": ["voter", "voter id", "election", "voting", "electoral"],
        "documents": ["Age and residence details plus supporting documents requested by the official form"],
        "url": "https://voters.eci.gov.in/",
        "note": "Check the official portal for current forms and eligibility rules."
    },
    {
        "name": "Public Grievances",
        "category": "Complaints & Help",
        "description": "Submit or track eligible public grievances through the central grievance portal.",
        "keywords": ["complaint", "grievance", "problem", "government complaint", "pgportal", "help"],
        "documents": ["Department/service details", "Complaint description and supporting reference numbers or files, if relevant"],
        "url": "https://pgportal.gov.in/",
        "note": "Some matters may be handled by state or local grievance portals instead."
    },
    {
        "name": "UMANG",
        "category": "Digital Services",
        "description": "Discover digital public services available through the UMANG platform.",
        "keywords": ["umang", "online service", "government app", "public services"],
        "documents": ["Account and verification details requested by the selected service"],
        "url": "https://web.umang.gov.in/",
        "note": "The services offered depend on the department and your eligibility."
    },
    {
        "name": "India.gov.in",
        "category": "Information",
        "description": "National portal for government information, services and resources.",
        "keywords": ["india portal", "government information", "central government", "services"],
        "documents": ["Varies by service; check the linked official department"],
        "url": "https://www.india.gov.in/",
        "note": "Use department links to verify current requirements."
    },
]

FAQS = [
    ("How do I find a government scheme?", "Start with MyScheme, enter relevant details, and read the official eligibility and application instructions. This assistant cannot guarantee eligibility."),
    ("What documents should I keep ready?", "Commonly requested documents may include identity, address, age, income, bank or academic details, depending on the service. Always use the exact checklist on the official portal."),
    ("Can this assistant submit an application for me?", "No. It provides guidance and official links only. You must review details and submit through the official service."),
    ("Is this an official government website?", "No. This is a student mini-project demonstration and is not affiliated with any government department."),
    ("What if I cannot find my service?", "Search by a keyword or open India.gov.in or UMANG to explore more services. You may also check your state government's official portal."),
]

def find_services(query, category="All categories"):
    q = query.lower().strip()
    results = []
    for service in SERVICES:
        if category != "All categories" and service["category"] != category:
            continue
        haystack = " ".join([service["name"], service["category"], service["description"], *service["keywords"]]).lower()
        words = [w for w in q.split() if len(w) > 1]
        score = sum(3 for w in words if w in service["name"].lower())
        score += sum(2 for w in words if w in service["keywords"])
        score += sum(1 for w in words if w in haystack)
        if not q:
            score = 1
        if score > 0:
            results.append((score, service))
    results.sort(key=lambda x: x[0], reverse=True)
    return [s for _, s in results]

st.title("🇮🇳 AI Citizen Services Assistant")
st.write("A simple guide to Indian public-service portals, schemes, document checklists, and citizen help.")
st.info("Student project demo — not an official government service. Never share OTPs, passwords, full Aadhaar/PAN numbers, or bank PINs here. Verify all details on official websites.")

tab1, tab2, tab3, tab4 = st.tabs(["🔎 Find a Service", "💬 Ask the Assistant", "✅ Document Checklist", "ℹ️ About"])

with tab1:
    st.subheader("Find the right public-service portal")
    left, right = st.columns([2, 1])
    with left:
        search = st.text_input("What do you need help with?", placeholder="e.g., scholarship, Aadhaar update, farmer scheme, voter ID")
    with right:
        categories = ["All categories"] + sorted(set(s["category"] for s in SERVICES))
        selected_category = st.selectbox("Filter by category", categories)
    matches = find_services(search, selected_category)
    if not search and selected_category == "All categories":
        matches = SERVICES
    if matches:
        for service in matches:
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"### {service['name']}")
                    st.caption(service["category"])
                    st.write(service["description"])
                    st.write("**Before you start:** " + service["note"])
                with c2:
                    st.link_button("Official portal ↗", service["url"], use_container_width=True)
    else:
        st.warning("No close match found. Try a shorter keyword such as 'passport', 'student', 'farmer', or 'complaint'.")

with tab2:
    st.subheader("Ask a question")
    st.write("Ask about common citizen services. The assistant matches your question to its service directory.")
    question = st.text_input("Your question", placeholder="How can I apply for a scholarship?")
    if st.button("Get guidance", type="primary"):
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            lower_q = question.lower()
            faq_matches = [x for x in FAQS if any(w in lower_q for w in x[0].lower().replace("?", "").split() if len(w) > 3)]
            if any(word in lower_q for word in ["document", "documents", "proof", "certificate"]):
                st.markdown("**General document guidance**")
                st.write("Common requirements may include identity, address, date-of-birth, income, bank or academic records. Requirements differ by service. Open the official portal and follow its current checklist.")
            matches = find_services(question)
            if matches:
                st.markdown("**Services that may help**")
                for service in matches[:4]:
                    st.markdown(f"- **{service['name']}** — {service['description']} [Open official portal]({service['url']})")
            if faq_matches:
                st.markdown("**Related guidance**")
                for q, a in faq_matches[:2]:
                    st.markdown(f"**{q}**")
                    st.write(a)
            if not matches and not faq_matches:
                st.write("I couldn't identify a close match. Try searching the service directory, or visit [India.gov.in](https://www.india.gov.in/) or [UMANG](https://web.umang.gov.in/).")
            st.caption("This is keyword-based demo guidance, not an official eligibility decision or legal advice.")

with tab3:
    st.subheader("Build a preparation checklist")
    chosen = st.selectbox("Choose a service", [s["name"] for s in SERVICES])
    service = next(s for s in SERVICES if s["name"] == chosen)
    st.write(f"**Service:** {service['description']}")
    st.write("Use these as preparation prompts, not a guaranteed final list.")
    for doc in service["documents"]:
        st.checkbox(doc, key=f"doc_{chosen}_{doc}")
    st.link_button("Verify requirements on official portal ↗", service["url"])
    st.caption("The official portal's latest instructions always take priority over this sample checklist.")

with tab4:
    st.subheader("Project details")
    st.markdown("""
**Objective:** Make it easier for citizens to discover public-service portals and prepare for applications.

**Technologies:** Python, Streamlit, pandas.

**How it works:**
1. The user enters a query or selects a category.
2. A keyword-matching algorithm ranks relevant service records.
3. The app displays descriptions, preparation prompts and official links.
4. The user verifies requirements and completes any application on the official portal.

**Limitations:** This demo uses a small curated directory and a rule-based matching algorithm. It does not connect to government databases, verify personal eligibility, submit applications, or guarantee that every listed requirement is current.
""")
    st.write(f"Directory entries: **{len(SERVICES)}**")
    st.write("Last opened app session:", datetime.now().strftime("%d %b %Y, %I:%M %p"))

st.divider()
st.caption("Use official portals for current information. This demonstration is not affiliated with the Government of India.")
