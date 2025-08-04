class JobSearchApp {
  constructor() {
    this.currentLatexContent = ""
    this.currentLetterContent = ""
    this.init()
  }

  init() {
    this.setupTabs()
    this.setupForms()
    this.setupFileUploads()
  }

  setupTabs() {
    const tabBtns = document.querySelectorAll(".tab-btn")
    const tabContents = document.querySelectorAll(".tab-content")

    tabBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const targetTab = btn.getAttribute("data-tab")

        // Remove active class from all tabs and contents
        tabBtns.forEach((b) => b.classList.remove("active"))
        tabContents.forEach((c) => c.classList.remove("active"))

        // Add active class to clicked tab and corresponding content
        btn.classList.add("active")
        document.getElementById(targetTab).classList.add("active")
      })
    })
  }

  setupForms() {
    // Job Search Form
    const jobSearchForm = document.getElementById("job-search-form")
    jobSearchForm.addEventListener("submit", (e) => {
      e.preventDefault()
      this.handleJobSearch()
    })

    // CV Generator Form
    const cvGeneratorForm = document.getElementById("cv-generator-form")
    cvGeneratorForm.addEventListener("submit", (e) => {
      e.preventDefault()
      this.handleCVGeneration()
    })

    // Cover Letter Form
    const coverLetterForm = document.getElementById("cover-letter-form")
    coverLetterForm.addEventListener("submit", (e) => {
      e.preventDefault()
      this.handleCoverLetterGeneration()
    })

    // Download and Copy buttons
    document.getElementById("download-latex")?.addEventListener("click", () => {
      this.downloadLatex()
    })

    document.getElementById("copy-latex")?.addEventListener("click", () => {
      this.copyToClipboard(this.currentLatexContent)
    })

    document.getElementById("copy-letter")?.addEventListener("click", () => {
      this.copyToClipboard(this.currentLetterContent)
    })
  }

  setupFileUploads() {
    const fileInputs = document.querySelectorAll(".file-input")

    fileInputs.forEach((input) => {
      const uploadArea = input.closest(".file-upload-area")

      // Click to upload
      uploadArea.addEventListener("click", () => {
        input.click()
      })

      // File selection
      input.addEventListener("change", (e) => {
        const file = e.target.files[0]
        if (file) {
          this.updateFileUploadText(uploadArea, file.name)
        }
      })

      // Drag and drop
      uploadArea.addEventListener("dragover", (e) => {
        e.preventDefault()
        uploadArea.classList.add("dragover")
      })

      uploadArea.addEventListener("dragleave", () => {
        uploadArea.classList.remove("dragover")
      })

      uploadArea.addEventListener("drop", (e) => {
        e.preventDefault()
        uploadArea.classList.remove("dragover")

        const files = e.dataTransfer.files
        if (files.length > 0) {
          input.files = files
          this.updateFileUploadText(uploadArea, files[0].name)
        }
      })
    })
  }

  updateFileUploadText(uploadArea, filename) {
    const textElement = uploadArea.querySelector(".file-upload-text p")
    textElement.innerHTML = `<i class="fas fa-check-circle"></i> ${filename}`
    textElement.style.color = "#38a169"
  }

  async handleJobSearch() {
    const formData = new FormData(document.getElementById("job-search-form"))
    const data = Object.fromEntries(formData)

    this.showLoading()

    try {
      const response = await fetch("/api/search-jobs", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })

      const result = await response.json()

      if (result.success) {
        this.displayJobResults(result.data)
      } else {
        this.showError("Erreur lors de la recherche: " + result.error)
      }
    } catch (error) {
      this.showError("Erreur de connexion: " + error.message)
    } finally {
      this.hideLoading()
    }
  }

  async handleCVGeneration() {
    const formData = new FormData(document.getElementById("cv-generator-form"))

    this.showLoading()

    try {
      const response = await fetch("/api/generate-cv", {
        method: "POST",
        body: formData,
      })

      const result = await response.json()

      if (result.success) {
        this.displayCVResults(result.data)
      } else {
        this.showError("Erreur lors de la génération: " + result.error)
      }
    } catch (error) {
      this.showError("Erreur de connexion: " + error.message)
    } finally {
      this.hideLoading()
    }
  }

  async handleCoverLetterGeneration() {
    const formData = new FormData(document.getElementById("cover-letter-form"))

    this.showLoading()

    try {
      const response = await fetch("/api/generate-cover-letter", {
        method: "POST",
        body: formData,
      })

      const result = await response.json()

      if (result.success) {
        this.displayCoverLetterResults(result.data)
      } else {
        this.showError("Erreur lors de la génération: " + result.error)
      }
    } catch (error) {
      this.showError("Erreur de connexion: " + error.message)
    } finally {
      this.hideLoading()
    }
  }

  displayJobResults(data) {
    const resultsSection = document.getElementById("job-results")
    const resultsContent = document.getElementById("job-results-content")

    // Parse the AI response to extract job information
    const jobsHTML = `
            <div class="info-message">
                <i class="fas fa-info-circle"></i>
                <strong>Résultats de recherche générés par l'IA</strong>
            </div>
            <div class="job-results-content">
                ${this.formatAIResponse(data)}
            </div>
        `

    resultsContent.innerHTML = jobsHTML
    resultsSection.style.display = "block"
    resultsSection.scrollIntoView({ behavior: "smooth" })
  }

  displayCVResults(data) {
    const resultsSection = document.getElementById("cv-results")
    const resultsContent = document.getElementById("cv-results-content")

    // Extract LaTeX code from AI response
    this.currentLatexContent = this.extractLatexFromResponse(data)

    const cvHTML = `
            <div class="success-message">
                <i class="fas fa-check-circle"></i>
                <strong>CV généré avec succès !</strong> Optimisé pour les systèmes ATS.
            </div>
            <div class="code-block">
                <pre>${this.escapeHtml(this.currentLatexContent)}</pre>
            </div>
            <div class="info-message">
                <i class="fas fa-lightbulb"></i>
                <strong>Instructions:</strong> Copiez le code LaTeX et collez-le dans Overleaf pour compiler votre CV.
            </div>
        `

    resultsContent.innerHTML = cvHTML
    resultsSection.style.display = "block"
    resultsSection.scrollIntoView({ behavior: "smooth" })
  }

  displayCoverLetterResults(data) {
    const resultsSection = document.getElementById("letter-results")
    const resultsContent = document.getElementById("letter-results-content")

    this.currentLetterContent = this.extractLetterFromResponse(data)

    const letterHTML = `
            <div class="success-message">
                <i class="fas fa-check-circle"></i>
                <strong>Lettre de motivation générée avec succès !</strong>
            </div>
            <div class="letter-content">
                ${this.formatLetterContent(this.currentLetterContent)}
            </div>
        `

    resultsContent.innerHTML = letterHTML
    resultsSection.style.display = "block"
    resultsSection.scrollIntoView({ behavior: "smooth" })
  }

  formatAIResponse(response) {
    // Format the AI response for better display
    if (typeof response === "string") {
      return `<div class="ai-response">${response.replace(/\n/g, "<br>")}</div>`
    }
    return `<div class="ai-response">${JSON.stringify(response, null, 2)}</div>`
  }

  extractLatexFromResponse(response) {
    // Extract LaTeX code from AI response
    const latexMatch = response.match(/\\documentclass[\s\S]*\\end\{document\}/)
    if (latexMatch) {
      return latexMatch[0]
    }

    // If no complete LaTeX document found, return the full response
    return response
  }

  extractLetterFromResponse(response) {
    // Extract letter content from AI response
    if (typeof response === "string") {
      return response
    }
    return JSON.stringify(response, null, 2)
  }

  formatLetterContent(content) {
    return content.replace(/\n/g, "<br>")
  }

  async downloadLatex() {
    if (!this.currentLatexContent) {
      this.showError("Aucun contenu LaTeX à télécharger")
      return
    }

    try {
      const response = await fetch("/api/download-latex", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          latex_content: this.currentLatexContent,
          filename: "cv_optimise.tex",
        }),
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement("a")
        a.href = url
        a.download = "cv_optimise.tex"
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)

        this.showSuccess("Fichier LaTeX téléchargé avec succès !")
      } else {
        this.showError("Erreur lors du téléchargement")
      }
    } catch (error) {
      this.showError("Erreur lors du téléchargement: " + error.message)
    }
  }

  async copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text)
      this.showSuccess("Contenu copié dans le presse-papiers !")
    } catch (error) {
      this.showError("Erreur lors de la copie: " + error.message)
    }
  }

  escapeHtml(text) {
    const div = document.createElement("div")
    div.textContent = text
    return div.innerHTML
  }

  showLoading() {
    document.getElementById("loading-overlay").style.display = "flex"
  }

  hideLoading() {
    document.getElementById("loading-overlay").style.display = "none"
  }

  showSuccess(message) {
    this.showMessage(message, "success")
  }

  showError(message) {
    this.showMessage(message, "error")
  }

  showMessage(message, type) {
    const messageDiv = document.createElement("div")
    messageDiv.className = `${type}-message`
    messageDiv.innerHTML = `
            <i class="fas fa-${type === "success" ? "check-circle" : "exclamation-triangle"}"></i>
            ${message}
        `

    // Insert at the top of the active tab content
    const activeTab = document.querySelector(".tab-content.active .card")
    activeTab.insertBefore(messageDiv, activeTab.firstChild)

    // Remove after 5 seconds
    setTimeout(() => {
      messageDiv.remove()
    }, 5000)
  }
}

// Initialize the app when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new JobSearchApp()
})
