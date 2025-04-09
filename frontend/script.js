// Main JavaScript for AutoQuoter

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const generateBtn = document.getElementById('generate-btn');
    const downloadBtn = document.getElementById('download-btn');
    const preview = document.getElementById('preview');
    const themeSelect = document.getElementById('theme');
    const customQuoteInput = document.getElementById('custom-quote');
    const removeWatermarkCheckbox = document.getElementById('removeWatermark');
    const loadingIndicator = document.getElementById('loading');
    const themeToggle = document.getElementById('theme-toggle-checkbox');
    const quoteTextContainer = document.getElementById('quote-text-container');
    const quoteText = document.getElementById('quote-text');
    const quoteAuthor = document.getElementById('quote-author');
    const copyQuoteBtn = document.getElementById('copy-quote-btn');
    const placeholder = document.getElementById('placeholder');
    const quotaCounter = document.getElementById('quota-count');
    
    // Premium modal elements
    const premiumModal = document.getElementById('premium-modal');
    const quotaLimitModal = document.getElementById('quota-limit-modal');
    const paymentSuccessModal = document.getElementById('payment-success-modal');
    const upgradeBtn = document.getElementById('upgrade-btn');
    const upgradeLink = document.getElementById('upgrade-link');
    const quotaUpgradeBtn = document.getElementById('quota-upgrade-btn');
    const successContinueBtn = document.getElementById('success-continue-btn');
    const closeModalButtons = document.querySelectorAll('.close-modal');
    const paymentMethods = document.querySelectorAll('.payment-method');
    const paymentForms = document.querySelectorAll('.payment-form');
    const payButtons = document.querySelectorAll('.pay-btn');
    
    // Base URL for backend API
    const apiUrl = '/api';
    
    // Store current quote data
    let currentQuoteData = {
        text: '',
        author: ''
    };
    
    // User quota tracking (stored in localStorage)
    let userQuota = {
        remaining: 5,
        isPremium: false,
        total: 5
    };
    
    // Load user quota from localStorage
    loadUserQuota();
    
    // Event listeners
    generateBtn.addEventListener('click', generateQuote);
    downloadBtn.addEventListener('click', downloadImage);
    themeToggle.addEventListener('change', toggleTheme);
    copyQuoteBtn.addEventListener('click', copyQuoteToClipboard);
    upgradeBtn.addEventListener('click', openPremiumModal);
    upgradeLink.addEventListener('click', function(e) {
        e.preventDefault();
        openPremiumModal();
    });
    quotaUpgradeBtn.addEventListener('click', function() {
        closeModal(quotaLimitModal);
        openPremiumModal();
    });
    successContinueBtn.addEventListener('click', function() {
        closeModal(paymentSuccessModal);
    });
    
    // Close modal buttons
    closeModalButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            closeModal(modal);
        });
    });
    
    // Payment method selection
    paymentMethods.forEach(method => {
        method.addEventListener('click', function() {
            // Remove active class from all methods
            paymentMethods.forEach(m => m.classList.remove('active'));
            // Add active class to selected method
            this.classList.add('active');
            
            // Hide all payment forms
            paymentForms.forEach(form => form.classList.add('hidden'));
            
            // Show the selected payment form
            const paymentMethod = this.getAttribute('data-method');
            document.getElementById(`${paymentMethod}-form`).classList.remove('hidden');
        });
    });
    
    // Payment button click handlers
    payButtons.forEach(btn => {
        btn.addEventListener('click', processDummyPayment);
    });
    
    // Load saved theme preference
    loadThemePreference();
    
    // Update quota display
    updateQuotaDisplay();
    
    // Generate quote function
    async function generateQuote() {
        // Check if user has quota remaining
        if (!userQuota.isPremium && userQuota.remaining <= 0) {
            openQuotaLimitModal();
            return;
        }
        
        try {
            // Show loading indicator and disable generate button
            loadingIndicator.classList.remove('hidden');
            generateBtn.disabled = true;
            preview.classList.add('hidden');
            placeholder.classList.add('hidden');
            downloadBtn.disabled = true;
            quoteTextContainer.classList.add('hidden');
            
            // Get theme and custom quote
            const theme = themeSelect.value;
            const customQuote = customQuoteInput.value.trim();
            const removeWatermark = userQuota.isPremium && removeWatermarkCheckbox.checked;
            
            // Prepare request data
            const requestData = {
                theme,
                removeWatermark
            };
            
            // Add custom quote if provided
            if (customQuote) {
                requestData.customQuote = customQuote;
                // Store custom quote data
                currentQuoteData = {
                    text: customQuote,
                    author: "Custom Quote"
                };
            } else {
                // Clear current quote data (will be updated later)
                currentQuoteData = {
                    text: '',
                    author: ''
                };
                
                // If it's a custom quote, we already know the text
                // If not, we'll fetch a quote from the API and need to also get it for display
                try {
                    // Make a separate request to get quote text
                    const quoteResponse = await fetch(`${apiUrl}/quota`, {
                        method: 'GET'
                    });
                    
                    // We don't actually use the quota, but this is a placeholder for 
                    // where we'd get quote text from a separate API call if needed
                    // For now, we'll just make something up based on the theme
                    
                    // This is a fallback for demo purposes
                    const quotes = {
                        "motivation": {
                            text: "The only way to do great work is to love what you do.",
                            author: "Steve Jobs"
                        },
                        "stoicism": {
                            text: "The obstacle is the way.",
                            author: "Marcus Aurelius"
                        },
                        "success": {
                            text: "Success is not final, failure is not fatal: It is the courage to continue that counts.",
                            author: "Winston Churchill"
                        },
                        "leadership": {
                            text: "Leadership is the capacity to translate vision into reality.",
                            author: "Warren Bennis"
                        },
                        "happiness": {
                            text: "Happiness is not something ready-made. It comes from your own actions.",
                            author: "Dalai Lama"
                        }
                    };
                    
                    currentQuoteData = quotes[theme] || quotes["motivation"];
                } catch (error) {
                    console.error("Error fetching quote text:", error);
                    // Use a generic quote as fallback
                    currentQuoteData = {
                        text: "The best preparation for tomorrow is doing your best today.",
                        author: "H. Jackson Brown Jr."
                    };
                }
            }
            
            // Make API request for image generation
            const response = await fetch(`${apiUrl}/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
            
            // Handle response
            if (response.ok) {
                const imageBlob = await response.blob();
                const imageUrl = URL.createObjectURL(imageBlob);
                
                // Show preview image
                preview.src = imageUrl;
                preview.classList.remove('hidden');
                downloadBtn.disabled = false;
                
                // Store blob for download
                preview.dataset.blob = imageUrl;
                
                // Update and show quote text container
                updateQuoteTextDisplay();
                
                // Decrement quota if not premium
                if (!userQuota.isPremium) {
                    userQuota.remaining--;
                    saveUserQuota();
                    updateQuotaDisplay();
                }
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.message || 'Failed to generate quote image'}`);
            }
        } catch (error) {
            console.error('Error generating quote:', error);
            alert('Error generating quote. Please try again.');
        } finally {
            // Hide loading indicator and enable generate button
            loadingIndicator.classList.add('hidden');
            generateBtn.disabled = false;
        }
    }
    
    // Update quote text display
    function updateQuoteTextDisplay() {
        if (currentQuoteData.text) {
            quoteText.textContent = `"${currentQuoteData.text}"`;
            quoteAuthor.textContent = `— ${currentQuoteData.author}`;
            quoteTextContainer.classList.remove('hidden');
        } else {
            quoteTextContainer.classList.add('hidden');
        }
    }
    
    // Copy quote to clipboard
    function copyQuoteToClipboard() {
        const textToCopy = `"${currentQuoteData.text}" — ${currentQuoteData.author}`;
        
        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                // Show feedback to user
                const originalText = copyQuoteBtn.textContent;
                copyQuoteBtn.textContent = "Copied!";
                setTimeout(() => {
                    copyQuoteBtn.textContent = originalText;
                }, 2000);
            })
            .catch(err => {
                console.error('Failed to copy text: ', err);
                alert('Failed to copy to clipboard. Please try again.');
            });
    }
    
    // Download image function
    function downloadImage() {
        if (preview.src) {
            const a = document.createElement('a');
            a.href = preview.dataset.blob;
            a.download = `autoquoter-${new Date().getTime()}.png`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    }
    
    // Toggle theme function
    function toggleTheme() {
        const isDarkMode = themeToggle.checked;
        const theme = isDarkMode ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }
    
    // Load theme preference from localStorage
    function loadThemePreference() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        
        if (savedTheme === 'dark') {
            themeToggle.checked = true;
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            themeToggle.checked = false;
            document.documentElement.setAttribute('data-theme', 'light');
        }
    }
    
    // Update quota display
    function updateQuotaDisplay() {
        quotaCounter.textContent = userQuota.remaining;
        if (userQuota.isPremium) {
            quotaCounter.textContent = "∞";
            document.querySelector('.quota-counter').innerHTML = 
                `<span id="quota-count" class="premium-badge">Premium</span> Unlimited quotes`;
            removeWatermarkCheckbox.disabled = false;
        }
    }
    
    // Load user quota from localStorage
    function loadUserQuota() {
        const savedQuota = JSON.parse(localStorage.getItem('userQuota'));
        if (savedQuota) {
            userQuota = savedQuota;
        } else {
            userQuota = {
                remaining: 5,
                isPremium: false,
                total: 5
            };
            saveUserQuota();
        }
    }
    
    // Save user quota to localStorage
    function saveUserQuota() {
        localStorage.setItem('userQuota', JSON.stringify(userQuota));
    }
    
    // Reset user quota (only used for testing)
    function resetUserQuota() {
        userQuota = {
            remaining: 5,
            isPremium: false,
            total: 5
        };
        saveUserQuota();
        updateQuotaDisplay();
    }
    
    // Open the premium upgrade modal
    function openPremiumModal() {
        openModal(premiumModal);
    }
    
    // Open the quota limit modal
    function openQuotaLimitModal() {
        openModal(quotaLimitModal);
    }
    
    // Open a modal
    function openModal(modal) {
        modal.classList.remove('hidden');
        setTimeout(() => {
            modal.classList.add('active');
        }, 10);
    }
    
    // Close a modal
    function closeModal(modal) {
        modal.classList.remove('active');
        setTimeout(() => {
            modal.classList.add('hidden');
        }, 300);
    }
    
    // Process dummy payment
    function processDummyPayment() {
        // Close the premium modal
        closeModal(premiumModal);
        
        // Simulate payment processing
        setTimeout(() => {
            // Upgrade user to premium
            userQuota.isPremium = true;
            userQuota.remaining = Infinity;
            saveUserQuota();
            updateQuotaDisplay();
            
            // Enable premium features
            removeWatermarkCheckbox.disabled = false;
            
            // Show success modal
            openModal(paymentSuccessModal);
        }, 1500);
    }
    
    // Initialize
    function initializeApp() {
        // Check premium status and update UI
        updateQuotaDisplay();
        removeWatermarkCheckbox.disabled = !userQuota.isPremium;
    }
    
    // Start the app
    initializeApp();
});