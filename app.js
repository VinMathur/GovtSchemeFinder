document.getElementById('schemeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Reset previous error messages
    clearErrors();
    
    // Collect form data
    const formData = {
        fullName: document.getElementById('fullName').value.trim(),
        age: document.getElementById('age').value,
        gender: document.getElementById('gender').value,
        contactNumber: document.getElementById('contactNumber').value,
        email: document.getElementById('email').value,
        aadhaarNumber: document.getElementById('aadhaarNumber').value,
        
        state: document.getElementById('state').value,
        district: document.getElementById('district').value,
        pinCode: document.getElementById('pinCode').value,
        
        annualIncome: document.getElementById('annualIncome').value,
        employmentStatus: document.getElementById('employmentStatus').value,
        bplCardStatus: document.getElementById('bplCardStatus').value,
        
        socialCategory: document.getElementById('socialCategory').value,
        disabilityStatus: document.getElementById('disabilityStatus').value,
        educationLevel: document.getElementById('educationLevel').value
    };

    // Validation
    const errors = validateForm(formData);
    
    if (Object.keys(errors).length > 0) {
        displayErrors(errors);
        return;
    }

    try {
        const response = await fetch('/.netlify/functions/find-schemes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const results = await response.json();

        // Check for rate limit error
        if (results.limit_reached) {
            document.getElementById('resultsContainer').innerHTML = `
                <div class="rate-limit-error">
                    <h3>Daily Query Limit Reached</h3>
                    <p>${results.message}</p>
                    <p>You are allowed only 4 queries per day. Please try again tomorrow.</p>
                </div>
            `;
            return;
        }

        displayResults(results);
    } catch (error) {
        console.error('Error fetching schemes:', error);
        document.getElementById('resultsContainer').innerHTML = 
            '<p class="error">Error fetching schemes. Please try again later.</p>';
    }
});

function validateForm(data) {
    const errors = {};

    // Full Name Validation
    if (!data.fullName) {
        errors.fullName = "Full Name is required";
    } else if (data.fullName.length < 2) {
        errors.fullName = "Full Name must be at least 2 characters long";
    }

    // Age Validation
    if (!data.age) {
        errors.age = "Age is required";
    } else {
        const age = parseInt(data.age);
        if (isNaN(age) || age < 0 || age > 120) {
            errors.age = "Please enter a valid age between 0 and 120";
        }
    }

    // Gender Validation
    if (!data.gender) {
        errors.gender = "Gender selection is required";
    }

    // Optional Contact Number Validation
    if (data.contactNumber && data.contactNumber.trim() !== '') {
        const phoneRegex = /^[6-9]\d{9}$/;
        if (!phoneRegex.test(data.contactNumber)) {
            errors.contactNumber = "Please enter a valid 10-digit mobile number";
        }
    }

    // Optional Email Validation
    if (data.email && data.email.trim() !== '') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(data.email)) {
            errors.email = "Please enter a valid email address";
        }
    }

    // Optional Aadhaar Number Validation
    if (data.aadhaarNumber && data.aadhaarNumber.trim() !== '') {
        const aadhaarRegex = /^\d{12}$/;
        if (!aadhaarRegex.test(data.aadhaarNumber)) {
            errors.aadhaarNumber = "Please enter a valid 12-digit Aadhaar Number";
        }
    }

    // State and District Validation
    if (!data.state) {
        errors.state = "State selection is required";
    }
    if (!data.district) {
        errors.district = "District selection is required";
    }

    // Pin Code Validation
    const pinCodeRegex = /^\d{6}$/;
    if (!data.pinCode) {
        errors.pinCode = "Pin Code is required";
    } else if (!pinCodeRegex.test(data.pinCode)) {
        errors.pinCode = "Please enter a valid 6-digit Pin Code";
    }

    // Annual Income Validation
    if (!data.annualIncome) {
        errors.annualIncome = "Annual Income is required";
    } else {
        const income = parseFloat(data.annualIncome);
        if (isNaN(income) || income < 0) {
            errors.annualIncome = "Please enter a valid annual income";
        }
    }

    // Dropdown Validations
    const requiredDropdowns = [
        'employmentStatus', 'bplCardStatus', 
        'socialCategory', 'disabilityStatus', 
        'educationLevel'
    ];

    requiredDropdowns.forEach(field => {
        if (!data[field]) {
            errors[field] = `${field.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())} is required`;
        }
    });

    return errors;
}

function displayErrors(errors) {
    Object.keys(errors).forEach(field => {
        const errorElement = document.getElementById(`${field}Error`);
        const inputElement = document.getElementById(field);
        
        if (errorElement) {
            errorElement.textContent = errors[field];
            errorElement.style.display = 'block';
        }
        
        if (inputElement) {
            inputElement.classList.add('error-input');
        }
    });
}

function clearErrors() {
    const errorElements = document.querySelectorAll('.error-message');
    const errorInputs = document.querySelectorAll('.error-input');
    
    errorElements.forEach(el => {
        el.textContent = '';
        el.style.display = 'none';
    });
    
    errorInputs.forEach(input => {
        input.classList.remove('error-input');
    });
}

function displayResults(schemes) {
    const resultsContainer = document.getElementById('resultsContainer');
    
    if (!schemes || schemes.length === 0) {
        resultsContainer.innerHTML = '<p>No matching schemes found.</p>';
        return;
    }

    resultsContainer.innerHTML = schemes.map(scheme => `
        <div class="scheme-result">
            <h3>${scheme.name || 'Unnamed Scheme'}</h3>
            <p>${scheme.description || 'No description available'}</p>
            <p><strong>Eligibility:</strong> ${scheme.eligibility || 'Not specified'}</p>
            ${scheme.applicationProcess ? `<p><strong>How to Apply:</strong> ${scheme.applicationProcess}</p>` : ''}
        </div>
    `).join('');
}