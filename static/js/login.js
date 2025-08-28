document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    const vendorForm = document.getElementById('vendor-form');
    const buyerForm = document.getElementById('buyer-form');
    
    // Initialize forms display
    if (vendorForm) vendorForm.style.display = 'block';
    if (buyerForm) buyerForm.style.display = 'none';
    
    // Add click event to tab buttons
    for (let i = 0; i < tabBtns.length; i++) {
        tabBtns[i].addEventListener('click', function() {
            // Remove active class from all buttons
            tabBtns.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Show the corresponding form
            const tabId = this.getAttribute('data-tab');
            
            if (tabId === 'vendor-form') {
                if (vendorForm) vendorForm.style.display = 'block';
                if (buyerForm) buyerForm.style.display = 'none';
            } else if (tabId === 'buyer-form') {
                if (vendorForm) vendorForm.style.display = 'none';
                if (buyerForm) buyerForm.style.display = 'block';
            }
        });
    }
    
    // Form submission handling
    const vendorRegistrationForm = document.getElementById('vendor-registration-form');
    const buyerRegistrationForm = document.getElementById('buyer-registration-form');
    
    // Function to show notification
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Hide notification after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 5000);
    }
    
    // Handle vendor registration form submission
    if (vendorRegistrationForm) {
        vendorRegistrationForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Validate password match
            const password = document.getElementById('vendor-password').value;
            const confirmPassword = document.getElementById('vendor-confirm-password').value;
            
            if (password !== confirmPassword) {
                showNotification('Passwords do not match', 'error');
                return;
            }
            
            // Create form data
            const formData = new FormData();
            formData.append('email', document.getElementById('vendor-email').value);
            formData.append('password', password);
            formData.append('mobile', document.getElementById('vendor-mobile').value);
            
            try {
                // Show loading state
                const submitBtn = vendorRegistrationForm.querySelector('button[type="submit"]');
                const originalText = submitBtn.textContent;
                submitBtn.textContent = 'Registering...';
                submitBtn.disabled = true;
                
                // Send data to server
                const response = await fetch('/register/vendor', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                // Reset button state
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                
                if (result.success) {
                    showNotification(result.message, 'success');
                    vendorRegistrationForm.reset();
                } else {
                    showNotification(result.message, 'error');
                }
            } catch (error) {
                showNotification('An error occurred. Please try again.', 'error');
                console.error('Error:', error);
            }
        });
    }
    
    // Handle buyer registration form submission
    if (buyerRegistrationForm) {
        buyerRegistrationForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Validate password match
            const password = document.getElementById('buyer-password').value;
            const confirmPassword = document.getElementById('buyer-confirm-password').value;
            
            if (password !== confirmPassword) {
                showNotification('Passwords do not match', 'error');
                return;
            }
            
            // Create form data
            const formData = new FormData();
            formData.append('email', document.getElementById('buyer-email').value);
            formData.append('password', password);
            formData.append('mobile', document.getElementById('buyer-mobile').value);
            
            try {
                // Show loading state
                const submitBtn = buyerRegistrationForm.querySelector('button[type="submit"]');
                const originalText = submitBtn.textContent;
                submitBtn.textContent = 'Registering...';
                submitBtn.disabled = true;
                
                // Send data to server
                const response = await fetch('/register/buyer', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                // Reset button state
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                
                if (result.success) {
                    showNotification(result.message, 'success');
                    buyerRegistrationForm.reset();
                } else {
                    showNotification(result.message, 'error');
                }
            } catch (error) {
                showNotification('An error occurred. Please try again.', 'error');
                console.error('Error:', error);
            }
        });
    }
    
    // Add submit button to vendor form if it doesn't exist
    if (vendorRegistrationForm && !vendorRegistrationForm.querySelector('button[type="submit"]')) {
        const submitBtn = document.createElement('button');
        submitBtn.type = 'submit';
        submitBtn.className = 'btn btn-primary';
        submitBtn.textContent = 'Register as Vendor';
        vendorRegistrationForm.appendChild(submitBtn);
    }
    
    // Add submit button to buyer form if it doesn't exist
    if (buyerRegistrationForm && !buyerRegistrationForm.querySelector('button[type="submit"]')) {
        const submitBtn = document.createElement('button');
        submitBtn.type = 'submit';
        submitBtn.className = 'btn btn-primary';
        submitBtn.textContent = 'Register as Buyer';
        buyerRegistrationForm.appendChild(submitBtn);
    }
    
    if (vendorRegistrationForm) {
        vendorRegistrationForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.textContent;
            submitBtn.textContent = 'Registering...';
            submitBtn.disabled = true;
            
            // Create FormData object
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/register/vendor', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Show success message
                    showNotification('Success! Your vendor account has been created.', 'success');
                    this.reset();
                } else {
                    // Show error message
                    showNotification(result.message || 'Registration failed. Please try again.', 'error');
                }
            } catch (error) {
                showNotification('An error occurred. Please try again later.', 'error');
                console.error('Error:', error);
            } finally {
                // Reset button state
                submitBtn.textContent = originalBtnText;
                submitBtn.disabled = false;
            }
        });
    }
    
    if (buyerRegistrationForm) {
        buyerRegistrationForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.textContent;
            submitBtn.textContent = 'Registering...';
            submitBtn.disabled = true;
            
            // Create FormData object
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/register/buyer', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Show success message
                    showNotification('Success! Your buyer account has been created.', 'success');
                    this.reset();
                } else {
                    // Show error message
                    showNotification(result.message || 'Registration failed. Please try again.', 'error');
                }
            } catch (error) {
                showNotification('An error occurred. Please try again later.', 'error');
                console.error('Error:', error);
            } finally {
                // Reset button state
                submitBtn.textContent = originalBtnText;
                submitBtn.disabled = false;
            }
        });
    }
    
    // Notification function
    function showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // Add to document
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Remove after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 5000);
    }
    
    // Countries data
    const countries = [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina", "Armenia", "Australia", 
        "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", 
        "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia", "Botswana", "Brazil", "Brunei", "Bulgaria", 
        "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Chad", "Chile", 
        "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", 
        "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", 
        "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Gabon", 
        "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", 
        "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", 
        "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", 
        "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", 
        "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", 
        "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", 
        "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", 
        "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", 
        "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", 
        "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent", "Samoa", "San Marino", 
        "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", 
        "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", 
        "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", 
        "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", 
        "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", 
        "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
    ];

    // Load countries
    function populateCountries(selectId) {
        const select = document.getElementById(selectId);
        if (!select) return;
        
        select.innerHTML = '<option value="">Select Country</option>';
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            select.appendChild(option);
        });
    }
    
    // Populate countries
    populateCountries('business-country');
    populateCountries('company-country');
    
    // Sample states data (simplified)
    const statesByCountry = {
        "United States": ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"],
        "India": ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"],
        "United Kingdom": ["England", "Northern Ireland", "Scotland", "Wales"],
        "Canada": ["Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Northwest Territories", "Nova Scotia", "Nunavut", "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan", "Yukon"],
        "Australia": ["Australian Capital Territory", "New South Wales", "Northern Territory", "Queensland", "South Australia", "Tasmania", "Victoria", "Western Australia"],
        "Pakistan": ["Balochistan", "Gilgit-Baltistan", "Islamabad Capital Territory", "Khyber Pakhtunkhwa", "Punjab", "Sindh", "Azad Kashmir"]
    };
    
    // Sample cities data (simplified)
    const citiesByState = {
        "California": ["Los Angeles", "San Francisco", "San Diego", "Sacramento", "San Jose"],
        "New York": ["New York City", "Buffalo", "Rochester", "Yonkers", "Syracuse"],
        "Texas": ["Houston", "San Antonio", "Dallas", "Austin", "Fort Worth"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik"],
        "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],
        "Punjab": ["Lahore", "Faisalabad", "Rawalpindi", "Multan", "Gujranwala"],
        "Sindh": ["Karachi", "Hyderabad", "Sukkur", "Larkana", "Mirpur Khas"]
    };
    
    // Load states based on country selection
    function loadStates(country, stateSelectId) {
        const stateSelect = document.getElementById(stateSelectId);
        if (!stateSelect) return;
        
        stateSelect.innerHTML = '<option value="">Select State</option>';
        
        if (statesByCountry[country]) {
            statesByCountry[country].forEach(state => {
                const option = document.createElement('option');
                option.value = state;
                option.textContent = state;
                stateSelect.appendChild(option);
            });
        }
    }
    
    // Load cities based on state selection
    function loadCities(state, citySelectId) {
        const citySelect = document.getElementById(citySelectId);
        if (!citySelect) return;
        
        citySelect.innerHTML = '<option value="">Select City</option>';
        
        if (citiesByState[state]) {
            citiesByState[state].forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                option.textContent = city;
                citySelect.appendChild(option);
            });
        }
    }
    
    // Country change event for business
    const businessCountry = document.getElementById('business-country');
    if (businessCountry) {
        businessCountry.addEventListener('change', function() {
            loadStates(this.value, 'business-state');
        });
    }
    
    // State change event for business
    const businessState = document.getElementById('business-state');
    if (businessState) {
        businessState.addEventListener('change', function() {
            loadCities(this.value, 'business-city');
        });
    }
    
    // Country change event for company
    const companyCountry = document.getElementById('company-country');
    if (companyCountry) {
        companyCountry.addEventListener('change', function() {
            loadStates(this.value, 'company-state');
        });
    }
    
    // State change event for company
    const companyState = document.getElementById('company-state');
    if (companyState) {
        companyState.addEventListener('change', function() {
            loadCities(this.value, 'company-city');
        });
    }
    
    // Add "Get Current Location" buttons
    function addLocationButtons() {
        const vendorAddressGroup = document.querySelector('#vendor-registration-form .form-group:has(#business-address)');
        const buyerAddressGroup = document.querySelector('#buyer-registration-form .form-group:has(#company-address)');
        
        if (vendorAddressGroup) {
            const locationBtn = document.createElement('button');
            locationBtn.type = 'button';
            locationBtn.className = 'btn btn-secondary location-btn';
            locationBtn.textContent = 'Get Current Location';
            locationBtn.onclick = function() { getCurrentLocation('business'); };
            vendorAddressGroup.appendChild(locationBtn);
        }
        
        if (buyerAddressGroup) {
            const locationBtn = document.createElement('button');
            locationBtn.type = 'button';
            locationBtn.className = 'btn btn-secondary location-btn';
            locationBtn.textContent = 'Get Current Location';
            locationBtn.onclick = function() { getCurrentLocation('company'); };
            buyerAddressGroup.appendChild(locationBtn);
        }
    }
    
    // Try to add location buttons
    try {
        addLocationButtons();
    } catch (e) {
        console.error('Error adding location buttons:', e);
    }
    
    // Get current location using Geolocation API
    function getCurrentLocation(prefix) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    
                    // Use OpenStreetMap Nominatim API for reverse geocoding
                    fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&zoom=18&addressdetails=1`)
                        .then(response => response.json())
                        .then(data => {
                            setLocationFields(data, prefix);
                        })
                        .catch(error => {
                            console.error('Error fetching location data:', error);
                            alert('Could not retrieve address information. Please enter manually.');
                        });
                },
                function(error) {
                    console.error('Geolocation error:', error);
                    alert('Could not get your location. Please enter address manually.');
                }
            );
        } else {
            alert('Geolocation is not supported by your browser. Please enter address manually.');
        }
    }
    
    // Set location fields based on geocoding result
    function setLocationFields(data, prefix) {
        const address = data.address || {};
        
        // Set address field
        const addressField = document.getElementById(`${prefix}-address`);
        if (addressField) {
            const streetAddress = [
                address.road || address.street || '',
                address.house_number || '',
                address.suburb || address.neighbourhood || ''
            ].filter(Boolean).join(', ');
            
            addressField.value = streetAddress;
        }
        
        // Set country
        const countryField = document.getElementById(`${prefix}-country`);
        if (countryField && address.country) {
            // Find and select the country option
            for (let i = 0; i < countryField.options.length; i++) {
                if (countryField.options[i].text === address.country) {
                    countryField.selectedIndex = i;
                    // Trigger change event to load states
                    const event = new Event('change');
                    countryField.dispatchEvent(event);
                    break;
                }
            }
        }
        
        // Set state/province
        setTimeout(() => {
            const stateField = document.getElementById(`${prefix}-state`);
            if (stateField && (address.state || address.province)) {
                const stateName = address.state || address.province;
                for (let i = 0; i < stateField.options.length; i++) {
                    if (stateField.options[i].text === stateName) {
                        stateField.selectedIndex = i;
                        // Trigger change event to load cities
                        const event = new Event('change');
                        stateField.dispatchEvent(event);
                        break;
                    }
                }
            }
            
            // Set city
            setTimeout(() => {
                const cityField = document.getElementById(`${prefix}-city`);
                if (cityField && address.city) {
                    for (let i = 0; i < cityField.options.length; i++) {
                        if (cityField.options[i].text === address.city) {
                            cityField.selectedIndex = i;
                            break;
                        }
                    }
                }
                
                // Set postal code
                const postalField = document.getElementById(`${prefix}-postal`);
                if (postalField && address.postcode) {
                    postalField.value = address.postcode;
                }
            }, 300);
        }, 300);
    }
    
    // Real-time validation for unique fields
    function debounce(func, delay) {
        let debounceTimer;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => func.apply(context, args), delay);
        };
    }
    
    // Check if email already exists
    const checkVendorEmail = debounce(function(email) {
        const errorElement = document.getElementById('vendor-email-error');
        
        // Simulate API call to check if email exists
        setTimeout(() => {
            if (email.includes('existing')) {
                errorElement.textContent = 'This email is already registered';
                errorElement.style.display = 'block';
            } else {
                errorElement.textContent = '';
                errorElement.style.display = 'none';
            }
        }, 500);
    }, 500);
    
    // Check if mobile already exists
    const checkVendorMobile = debounce(function(mobile) {
        const errorElement = document.getElementById('vendor-mobile-error');
        
        // Simulate API call to check if mobile exists
        setTimeout(() => {
            if (mobile.includes('123456')) {
                errorElement.textContent = 'This mobile number is already registered';
                errorElement.style.display = 'block';
            } else {
                errorElement.textContent = '';
                errorElement.style.display = 'none';
            }
        }, 500);
    }, 500);
    
    // Check if NTN already exists
    const checkVendorNTN = debounce(function(ntn) {
        const errorElement = document.getElementById('business-ntn-error');
        
        // Simulate API call to check if NTN exists
        setTimeout(() => {
            if (ntn.includes('12345')) {
                errorElement.textContent = 'This NTN is already registered';
                errorElement.style.display = 'block';
            } else {
                errorElement.textContent = '';
                errorElement.style.display = 'none';
            }
        }, 500);
    }, 500);
    
    // Check if buyer email already exists
    const checkBuyerEmail = debounce(function(email) {
        const errorElement = document.getElementById('buyer-email-error');
        
        // Simulate API call to check if email exists
        setTimeout(() => {
            if (email.includes('existing')) {
                errorElement.textContent = 'This email is already registered';
                errorElement.style.display = 'block';
            } else {
                errorElement.textContent = '';
                errorElement.style.display = 'none';
            }
        }, 500);
    }, 500);
    
    // Check if buyer mobile already exists
    const checkBuyerMobile = debounce(function(mobile) {
        const errorElement = document.getElementById('buyer-mobile-error');
        
        // Simulate API call to check if mobile exists
        setTimeout(() => {
            if (mobile.includes('123456')) {
                errorElement.textContent = 'This mobile number is already registered';
                errorElement.style.display = 'block';
            } else {
                errorElement.textContent = '';
                errorElement.style.display = 'none';
            }
        }, 500);
    }, 500);
    
    // Add event listeners for real-time validation
    const vendorEmail = document.getElementById('vendor-email');
    if (vendorEmail) {
        vendorEmail.addEventListener('input', function() {
            checkVendorEmail(this.value);
        });
    }
    
    const vendorMobile = document.getElementById('vendor-mobile');
    if (vendorMobile) {
        vendorMobile.addEventListener('input', function() {
            checkVendorMobile(this.value);
        });
    }
    
    const businessNTN = document.getElementById('business-ntn');
    if (businessNTN) {
        businessNTN.addEventListener('input', function() {
            checkVendorNTN(this.value);
        });
    }
    
    const buyerEmail = document.getElementById('buyer-email');
    if (buyerEmail) {
        buyerEmail.addEventListener('input', function() {
            checkBuyerEmail(this.value);
        });
    }
    
    const buyerMobile = document.getElementById('buyer-mobile');
    if (buyerMobile) {
        buyerMobile.addEventListener('input', function() {
            checkBuyerMobile(this.value);
        });
    }
});