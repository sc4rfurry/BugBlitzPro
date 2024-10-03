// Workflow designer
const app = new Vue({
    el: '#workflow-designer',
    data: {
        workflow: {
            steps: []
        },
        availableTools: [],
        csrfToken: ''
    },
    methods: {
        addStep() {
            this.workflow.steps.push({
                tool_id: '',
                arguments: ''
            });
        },
        removeStep(index) {
            this.workflow.steps.splice(index, 1);
        },
        saveWorkflow() {
            fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body: JSON.stringify({
                    steps: this.workflow.steps,
                    csrf_token: this.csrfToken
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Workflow saved successfully');
                } else {
                    alert('Error saving workflow');
                }
            });
        }
    },
    mounted() {
        this.csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        // Fetch available tools and existing workflow data
    }
});

// Add this function to get the CSRF token from the meta tag
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Use this function when making AJAX requests
fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => {
    // Handle the response
})
.catch(error => {
    console.error('Error:', error);
});