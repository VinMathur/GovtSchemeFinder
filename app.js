document.getElementById('schemeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Reset previous error messages
    clearErrors();
    
    // Collect form data
    const formData = {
        fullName: document.getElementById('fullName').value,
        age: document.getElementById('age').value,
        gender: document.getElementById('gender').value,
        contactNumber: document.getElementById('contactNumber').value || null,
        email: document.getElementById('email').value || null,
        aadhaarNumber: document.getElementById('aadhaarNumber').value || null,
        
        state: document.getElementById('state').value,
        district: document.getElementById('district').value,
        pinCode: document.getElementById('pinCode').value,
        
        annualIncome: document.getElementById('annualIncome').value,
        employmentStatus: document.getElementById('employmentStatus').value,
        bplCardStatus: document.getElementById('bplCardStatus').value,
        
        socialCategory: document.getElementById('socialCategory').value,
        disabilityStatus: document.getElementById('disabilityStatus').value,
        educationLevel: document.getElementById('educationLevel').value,
        
        // Business & Entrepreneurship Fields (Optional)
        businessStatus: document.getElementById('businessStatus')?.value || null,
        businessType: document.getElementById('businessType')?.value || null,
        investmentRange: document.getElementById('investmentRange')?.value || null,
        businessSector: document.getElementById('businessSector')?.value || null,
        previousExperience: document.getElementById('previousExperience')?.value || null,
        
        // Support Types (Dropdown)
        supportType: document.getElementById('supportType')?.selectedOptions 
            ? Array.from(document.getElementById('supportType').selectedOptions).map(option => option.value)
            : [],
        
        language: document.getElementById('language-select').value
    };

    // Validation (modify to make business details optional)
    const errors = validateForm(formData);
    
    if (Object.keys(errors).length > 0) {
        displayErrors(errors);
        return;
    }

    try {
        await findSchemes(formData);
    } catch (error) {
        console.error('Error fetching schemes:', error);
        document.getElementById('resultsContainer').innerHTML = 
            '<p class="error">Error fetching schemes. Please try again later.</p>';
    }
});

async function findSchemes(formData) {
    try {
        console.log('Sending form data:', formData);
        
        // Use relative path for local development, full URL for production
        const netlifyFunctionUrl = window.location.hostname === 'localhost' 
            ? '/.netlify/functions/find-schemes' 
            : 'https://govschemes.netlify.app/.netlify/functions/find-schemes';
        
        console.log('Netlify Function URL:', netlifyFunctionUrl);
        
        const response = await fetch(netlifyFunctionUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        console.log('Full response details:', {
            status: response.status,
            statusText: response.statusText,
            headers: Object.fromEntries(response.headers.entries()),
            url: response.url
        });

        // Handle different response scenarios
        if (!response.ok) {
            // Try to parse error response as JSON
            try {
                const errorBody = await response.text();
                let errorDetails = {};
                
                try {
                    errorDetails = JSON.parse(errorBody);
                } catch (parseError) {
                    console.warn('Could not parse error response as JSON:', parseError);
                }

                console.error('Server response error:', {
                    status: response.status,
                    statusText: response.statusText,
                    body: errorBody,
                    parsedDetails: errorDetails
                });

                // Detailed error message for user
                document.getElementById('resultsContainer').innerHTML = `
                    <div class="error-container">
                        <h3>Error Fetching Schemes</h3>
                        <p>${errorDetails.message || 'Unable to retrieve government schemes.'}</p>
                        <p>Debug Information:</p>
                        <ul>
                            <li>Status Code: ${response.status}</li>
                            <li>Status Text: ${response.statusText}</li>
                            <li>Response URL: ${response.url}</li>
                            <li>Error Details: ${JSON.stringify(errorDetails)}</li>
                        </ul>
                        <p>Possible reasons:</p>
                        <ul>
                            <li>Network connectivity issues</li>
                            <li>Netlify function not deployed correctly</li>
                            <li>API key or authentication problem</li>
                            <li>Daily query limit exceeded</li>
                        </ul>
                        <p>Please check your internet connection or try again later.</p>
                    </div>
                `;
                return;
            } catch (parseError) {
                console.error('Failed to parse error response:', parseError);
                
                // Fallback error message
                document.getElementById('resultsContainer').innerHTML = `
                    <div class="error-container">
                        <h3>Unexpected Error</h3>
                        <p>Unable to retrieve government schemes.</p>
                        <p>Status Code: ${response.status}</p>
                        <p>Please try again later.</p>
                    </div>
                `;
                return;
            }
        }

        // Parse successful response
        try {
            const results = await response.json();
            console.log('Received results:', results);

            // Check if results is an array and has content
            if (Array.isArray(results) && results.length > 0) {
                // Render schemes
                const schemesHtml = results.map(scheme => `
                    <div class="scheme-result">
                        <h3>${scheme.name || 'Unnamed Scheme'}</h3>
                        <p>${scheme.description || 'No description available'}</p>
                        ${scheme.eligibility ? `<p><strong>Eligibility:</strong> ${scheme.eligibility}</p>` : ''}
                        ${scheme.benefits ? `<p><strong>Benefits:</strong> ${scheme.benefits}</p>` : ''}
                        ${scheme.link ? `<a href="${scheme.link}" target="_blank" rel="noopener noreferrer">Learn More</a>` : ''}
                    </div>
                `).join('');

                document.getElementById('resultsContainer').innerHTML = `
                    <h2>Recommended Schemes</h2>
                    ${schemesHtml}
                `;
            } else {
                // No schemes found
                document.getElementById('resultsContainer').innerHTML = `
                    <div class="no-results">
                        <h3>No Schemes Found</h3>
                        <p>We couldn't find any government schemes matching your profile.</p>
                        <p>Try adjusting your search criteria or contact local government offices for more information.</p>
                    </div>
                `;
            }
        } catch (jsonError) {
            console.error('Failed to parse JSON response:', jsonError);
            
            document.getElementById('resultsContainer').innerHTML = `
                <div class="error-container">
                    <h3>Data Processing Error</h3>
                    <p>We received a response, but couldn't process the scheme information.</p>
                    <p>Please try again later.</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Comprehensive error in findSchemes:', {
            name: error.name,
            message: error.message,
            stack: error.stack,
            type: typeof error
        });
        
        document.getElementById('resultsContainer').innerHTML = `
            <div class="error-container">
                <h3>Network Error</h3>
                <p>Unable to connect to the server.</p>
                <p>Error Details: ${error.message}</p>
                <p>Possible reasons:</p>
                <ul>
                    <li>No internet connection</li>
                    <li>Server is down</li>
                    <li>Firewall or network restrictions</li>
                </ul>
                <p>Please check your internet connection and try again.</p>
            </div>
        `;
    }
}

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
        'educationLevel', 'language'
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
