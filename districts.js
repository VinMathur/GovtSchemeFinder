// Comprehensive mapping of states to districts
const stateDistrictMap = {
    "Andhra Pradesh": [
        "Srikakulam", "Vizianagaram", "Visakhapatnam", "East Godavari", 
        "West Godavari", "Krishna", "Guntur", "Prakasam", "Nellore", 
        "Chittoor", "Kadapa", "Anantapur", "Kurnool"
    ],
    "Arunachal Pradesh": [
        "Tawang", "West Kameng", "East Kameng", "Papum Pare", "Kurung Kumey", 
        "Kra Daadi", "Lower Subansiri", "Upper Subansiri", "West Siang", 
        "East Siang", "Siang", "Upper Dibang Valley", "Lower Dibang Valley", 
        "Dibang Valley", "Anjaw", "Lohit", "Namsai", "Changlang", "Tirap"
    ],
    "Assam": [
        "Baksa", "Barpeta", "Bieo", "Bongaigaon", "Cachar", "Chirang", 
        "Darrang", "Dhemaji", "Dhubri", "Dibrugarh", "Goalpara", "Golaghat", 
        "Hailakandi", "Jorhat", "Kamrup", "Kamrup Metropolitan", "Karbi Anglong", 
        "Karimganj", "Kokrajhar", "Lakhimpur", "Morigaon", "Nagaon", "Nalbari", 
        "Sivasagar", "Sonitpur", "Tinsukia", "Udalguri"
    ],
    "Bihar": [
        "Araria", "Arwal", "Aurangabad", "Banka", "Begusarai", "Bhagalpur", 
        "Bhojpur", "Buxar", "Darbhanga", "East Champaran", "Gaya", "Gopalganj", 
        "Jamui", "Jehanabad", "Kaimur", "Katihar", "Khagaria", "Kishanganj", 
        "Lakhisarai", "Madhepura", "Madhubani", "Munger", "Muzaffarpur", 
        "Nalanda", "Nawada", "Patna", "Purnia", "Rohtas", "Saharsa", 
        "Samastipur", "Saran", "Sheikhpura", "Sheohar", "Sitamarhi", 
        "Siwan", "Supaul", "Vaishali", "West Champaran"
    ],
    "Chhattisgarh": [
        "Balod", "Balrampur", "Bastar", "Bemetara", "Bigewar", "Dantewara", 
        "Dhamtari", "Durg", "Gariaband", "Jashpur", "Kabirdham", "Kanker", 
        "Kondagaon", "Korba", "Koriya", "Mahasamund", "Mungeli", "Narayanpur", 
        "Raigarh", "Raipur", "Rajnandgaon", "Sukma", "Surajpur", "Surguja"
    ],
    "Goa": [
        "North Goa", "South Goa"
    ],
    "Gujarat": [
        "Ahmedabad", "Amreli", "Anand", "Aravalli", "Banaskantha", "Bharuch", 
        "Bhavnagar", "Botad", "Chhota Udaipur", "Dahod", "Dang", "Devbhoomi Dwarka", 
        "Gandhinagar", "Gir Somnath", "Jamnagar", "Junagadh", "Kheda", "Kutch", 
        "Mahisagar", "Mehsana", "Morbi", "Narmada", "Navsari", "Panchmahal", 
        "Patan", "Porbandar", "Rajkot", "Sabarkantha", "Surat", "Tapi", 
        "Valsad"
    ],
    "Haryana": [
        "Ambala", "Bhiwani", "Charkhi Dadri", "Faridabad", "Fatehabad", 
        "Gurugram", "Hisar", "Jhajjar", "Jind", "Kaithal", "Karnal", "Kurukshetra", 
        "Mahendragarh", "Nuh", "Palwal", "Panchkula", "Panipat", "Rewari", 
        "Rohtak", "Sirsa", "Sonipat", "Yamunanagar"
    ],
    "Himachal Pradesh": [
        "Bilaspur", "Chamba", "Hamirpur", "Kangra", "Kinnaur", "Kullu", 
        "Lahaul and Spiti", "Mandi", "Shimla", "Sirmaur", "Solan", "Una"
    ],
    "Jharkhand": [
        "Bokaro", "Chatra", "Deoghar", "Dhanbad", "Dumka", "East Singhbhum", 
        "Garhwa", "Giridih", "Godda", "Gumla", "Hazaribagh", "Jamtara", 
        "Khunti", "Koderma", "Latehar", "Lohardaga", "Pakur", "Palamu", 
        "Ramgarh", "Ranchi", "Sahibganj", "Seraikela Kharsawan", "Simdega", 
        "West Singhbhum"
    ],
    "Karnataka": [
        "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban", 
        "Bidar", "Chamarajnagar", "Chikballapur", "Chikkamagaluru", "Chitradurga", 
        "Dakshina Kannada", "Davangere", "Dharwad", "Gadag", "Hassan", "Haveri", 
        "Kalaburagi", "Kodagu", "Kolar", "Koppal", "Mandya", "Mysuru", "Raichur", 
        "Ramanagara", "Shivamogga", "Tumakuru", "Udupi", "Uttara Kannada"
    ],
    "Kerala": [
        "Alappuzha", "Ernakulam", "Idukki", "Kannur", "Kasaragod", "Kollam", 
        "Kottayam", "Kozhikode", "Malappuram", "Palakkad", "Pathanamthitta", 
        "Thiruvananthapuram", "Thrissur", "Wayanad"
    ],
    "Madhya Pradesh": [
        "Agar", "Alirajpur", "Anuppur", "Ashoknagar", "Balaghat", "Barwani", 
        "Betul", "Bhind", "Bhopal", "Burhanpur", "Chhatarpur", "Chhindwara", 
        "Damoh", "Datiya", "Dewas", "Dhar", "Dindori", "Guna", "Gwalior", 
        "Harda", "Hoshangabad", "Indore", "Jabalpur", "Jhabua", "Katni", 
        "Khargone", "Mandla", "Mandsaur", "Morena", "Narsinghpur", "Neemuch", 
        "Panna", "Raisen", "Rajgarh", "Ratlam", "Rewa", "Sagar", "Satna", 
        "Sehore", "Seoni", "Shahdol", "Shajapur", "Sheopur", "Shivpuri", 
        "Sidhi", "Singrauli", "Tikamgarh", "Ujjain", "Umaria", "Vidisha"
    ],
    "Maharashtra": [
        "Mumbai City", "Mumbai Suburban", "Thane", "Pune", "Nagpur", "Nashik", 
        "Aurangabad", "Solapur", "Amravati", "Kolhapur", "Satara", "Ahmednagar", 
        "Yavatmal", "Nanded", "Jalgaon", "Akola", "Latur", "Sangli", "Buldhana", 
        "Chandrapur", "Dhule", "Gondia", "Hingoli", "Jalna", "Osmanabad", 
        "Parbhani", "Raigad", "Ratnagiri", "Washim", "Wardha"
    ],
    "Manipur": [
        "Bishnupur", "Chandel", "Churachandpur", "Imphal East", "Imphal West", 
        "Senapati", "Tamenglong", "Thoubal", "Ukhrul"
    ],
    "Meghalaya": [
        "East Garo Hills", "East Khasi Hills", "Jaintia Hills", "North Garo Hills", 
        "Ri Bhoi", "South Garo Hills", "South West Garo Hills", "West Garo Hills", 
        "West Khasi Hills"
    ],
    "Mizoram": [
        "Aizawl", "Champhai", "Kolasib", "Lawngtlai", "Lunglei", "Mamit", 
        "Saiha", "Serchhip"
    ],
    "Nagaland": [
        "Dimapur", "Kiphire", "Kohima", "Longleng", "Mokokchung", "Mon", 
        "Peren", "Phek", "Tuensang", "Wokha", "Zunheboto"
    ],
    "Odisha": [
        "Angul", "Balasore", "Baragarh", "Bhadrak", "Bolangir", "Boudh", 
        "Cuttack", "Deogarh", "Dhenkanal", "Gajapati", "Ganjam", "Jagatsinghpur", 
        "Jajpur", "Jharsuguda", "Kalahandi", "Kandhamal", "Kendrapara", 
        "Kendujhar", "Khordha", "Koraput", "Malkangiri", "Mayurbhanj", 
        "Nabarangpur", "Nayagarh", "Nuapada", "Puri", "Rayagada", "Sambalpur", 
        "Subarnapur", "Sundargarh"
    ],
    "Punjab": [
        "Amritsar", "Barnala", "Bathinda", "Faridkot", "Fatehgarh Sahib", 
        "Fazilka", "Firozpur", "Gurdaspur", "Hoshiarpur", "Jalandhar", 
        "Kapurthala", "Ludhiana", "Mansa", "Moga", "Mohali", "Muktsar", 
        "Pathankot", "Patiala", "Rupnagar", "Sangrur", "Tarn Taran"
    ],
    "Rajasthan": [
        "Ajmer", "Alwar", "Banswara", "Baran", "Barmer", "Bharatpur", 
        "Bhilwara", "Bikaner", "Bundi", "Chittorgarh", "Churu", "Dausa", 
        "Dholpur", "Dungarpur", "Hanumangarh", "Jaipur", "Jaisalmer", 
        "Jalore", "Jhalawar", "Jhunjhunu", "Jodhpur", "Karauli", "Kota", 
        "Nagaur", "Pali", "Pratapgarh", "Rajsamand", "Sawai Madhopur", 
        "Sikar", "Sirohi", "Sri Ganganagar", "Tonk", "Udaipur"
    ],
    "Sikkim": [
        "East Sikkim", "North Sikkim", "South Sikkim", "West Sikkim"
    ],
    "Tamil Nadu": [
        "Ariyalur", "Chennai", "Coimbatore", "Cuddalore", "Dharmapuri", 
        "Dindigul", "Erode", "Kancheepuram", "Karur", "Krishnagiri", 
        "Madurai", "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", 
        "Pudukkottai", "Ramanathapuram", "Salem", "Sivaganga", "Thanjavur", 
        "Theni", "Thiruvallur", "Thiruvarur", "Thoothukkudi", "Tiruchirappalli", 
        "Tirunelveli", "Tiruppur", "Tiruvanamalai", "Vellore", "Viluppuram", 
        "Virudhunagar"
    ],
    "Telangana": [
        "Adilabad", "Bhadradri Kothagudem", "Hyderabad", "Jagtial", "Jangaon", 
        "Jayashankar Bhupalapalli", "Jogulamba Gadwal", "Kamareddy", "Karimnagar", 
        "Khammam", "Kumuram Bheem", "Mahabubabad", "Mahabubnagar", "Mancherial", 
        "Medak", "Medchal-Malkajgiri", "Nagarkurnool", "Nalgonda", "Nirmal", 
        "Nizamabad", "Peddapalli", "Rajanna Sircilla", "Rangareddy", "Sangareddy", 
        "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy", "Warangal Rural", 
        "Warangal Urban", "Yadadri Bhuvanagiri"
    ],
    "Tripura": [
        "Dhalai", "Gomati", "Khowai", "North Tripura", "Sepahijala", 
        "South Tripura", "Unakoti", "West Tripura"
    ],
    "Uttar Pradesh": [
        "Agra", "Aligarh", "Allahabad", "Ambedkar Nagar", "Auraiya", "Azamgarh", 
        "Badaun", "Baghpat", "Bahraich", "Ballia", "Balrampur", "Banda", 
        "Barabanki", "Bareilly", "Basti", "Bijnor", "Bulandshahr", "Chandauli", 
        "Chitrakoot", "Deoria", "Etah", "Etawah", "Faizabad", "Fatehgarh", 
        "Fatehpur", "Firozabad", "Gautambudh Nagar", "Ghaziabad", "Ghazipur", 
        "Gonda", "Gorakhpur", "Hamirpur", "Hardoi", "Hathras", "Jalaun", 
        "Jaunpur", "Jhansi", "Kannauj", "Kanpur Dehat", "Kanpur Nagar", 
        "Kaushambi", "Khiri", "Kushi Nagar", "Lalitpur", "Lucknow", "Maharajganj", 
        "Mahoba", "Mainpuri", "Mathura", "Mau", "Meerut", "Mirzapur", "Moradabad", 
        "Muzaffarnagar", "Pilibhit", "Pratapgarh", "Raibareilly", "Rampur", 
        "Saharanpur", "Sant Kabirnagar", "Shahjahanpur", "Shrawasti", "Sidharthnagar", 
        "Sitapur", "Sonbhadra", "St. Ravidasnagar", "Sultanpur", "Unnao", "Varanasi"
    ],
    "Uttarakhand": [
        "Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun", "Haridwar", 
        "Nainital", "Pauri Garhwal", "Pithoragarh", "Rudra Prayag", "Tehri Garhwal", 
        "Udham Singh Nagar", "Uttarkashi"
    ],
    "West Bengal": [
        "Alipurduar", "Bankura", "Birbhum", "Cooch Behar", "Dakshin Dinajpur", 
        "Darjeeling", "East Midnapore", "Hooghly", "Howrah", "Jalpaiguri", 
        "Jhargram", "Kalimpong", "Kolkata", "Malda", "Murshidabad", "Nadia", 
        "North 24 Parganas", "Paschim Midnapore", "Purulia", "South 24 Parganas", 
        "Uttar Dinajpur"
    ],
    // Union Territories
    "Andaman and Nicobar Islands": [
        "Andaman", "Nicobar"
    ],
    "Chandigarh": [
        "Chandigarh"
    ],
    "Dadra and Nagar Haveli and Daman and Diu": [
        "Dadra and Nagar Haveli", "Daman", "Diu"
    ],
    "Delhi": [
        "Central Delhi", "East Delhi", "New Delhi", "North Delhi", 
        "North East Delhi", "North West Delhi", "Shahdara", "South Delhi", 
        "South East Delhi", "South West Delhi", "West Delhi"
    ],
    "Jammu and Kashmir": [
        "Anantnag", "Bandipora", "Baramulla", "Budgam", "Doda", "Ganderbal", 
        "Jammu", "Kargil", "Kathua", "Kishtwar", "Kulgam", "Kupwara", "Leh", 
        "Pulwama", "Rajouri", "Ramban", "Reasi", "Samba", "Shopian", "Srinagar", 
        "Tral", "Udhampur"
    ],
    "Ladakh": [
        "Kargil", "Leh"
    ],
    "Lakshadweep": [
        "Lakshadweep"
    ],
    "Puducherry": [
        "Karaikal", "Puducherry", "Yanam"
    ]
};

document.getElementById('state').addEventListener('change', function() {
    const districtSelect = document.getElementById('district');
    const selectedState = this.value;

    console.log('Selected State:', selectedState);
    console.log('Available States:', Object.keys(stateDistrictMap));

    // Reset district dropdown
    districtSelect.innerHTML = '<option value="">Select District</option>';
    districtSelect.disabled = true;

    if (selectedState && stateDistrictMap[selectedState]) {
        console.log('Districts for', selectedState, ':', stateDistrictMap[selectedState]);

        // Populate districts for selected state
        stateDistrictMap[selectedState].forEach(district => {
            const option = document.createElement('option');
            option.value = district;
            option.textContent = district;
            districtSelect.appendChild(option);
        });

        districtSelect.disabled = false;
    } else {
        console.warn('No districts found for state:', selectedState);
    }
});
