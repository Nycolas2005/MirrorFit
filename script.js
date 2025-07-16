class MirrorFitApp {
  constructor() {
    this.selectedClothing = {
      shirt: null,
      pants: null,
      shorts: null,
      shoes: null,
    }
    this.uploadedPhoto = null
    this.initializeEventListeners()
  }

  initializeEventListeners() {
    // Upload functionality
    const uploadArea = document.getElementById("uploadArea")
    const photoInput = document.getElementById("photoInput")
    const removePhoto = document.getElementById("removePhoto")

    uploadArea.addEventListener("click", () => photoInput.click())
    uploadArea.addEventListener("dragover", this.handleDragOver.bind(this))
    uploadArea.addEventListener("drop", this.handleDrop.bind(this))
    photoInput.addEventListener("change", this.handleFileSelect.bind(this))
    removePhoto.addEventListener("click", this.removePhoto.bind(this))

    // Clothing selection
    const clothingItems = document.querySelectorAll(".clothing-item")
    clothingItems.forEach((item) => {
      item.addEventListener("click", this.selectClothing.bind(this))
    })

    // Try on button
    const tryOnBtn = document.getElementById("tryOnBtn")
    tryOnBtn.addEventListener("click", this.tryOnClothes.bind(this))

    // Result actions
    const tryAgainBtn = document.getElementById("tryAgainBtn")
    const saveResultBtn = document.getElementById("saveResultBtn")

    tryAgainBtn.addEventListener("click", this.tryAgain.bind(this))
    saveResultBtn.addEventListener("click", this.saveResult.bind(this))
  }

  handleDragOver(e) {
    e.preventDefault()
    e.currentTarget.classList.add("dragover")
  }

  handleDrop(e) {
    e.preventDefault()
    e.currentTarget.classList.remove("dragover")
    const files = e.dataTransfer.files
    if (files.length > 0) {
      this.processFile(files[0])
    }
  }

  handleFileSelect(e) {
    const file = e.target.files[0]
    if (file) {
      this.processFile(file)
    }
  }

  processFile(file) {
    if (!file.type.startsWith("image/")) {
      alert("Por favor, selecione apenas arquivos de imagem.")
      return
    }

    if (file.size > 5 * 1024 * 1024) {
      alert("O arquivo deve ter no máximo 5MB.")
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      this.uploadedPhoto = file // Armazenar o arquivo original
      this.showPhotoPreview(e.target.result)
      this.updateTryOnButton()
    }
    reader.readAsDataURL(file)
  }

  showPhotoPreview(imageSrc) {
    const uploadArea = document.getElementById("uploadArea")
    const photoPreview = document.getElementById("photoPreview")
    const previewImage = document.getElementById("previewImage")

    uploadArea.style.display = "none"
    photoPreview.style.display = "block"
    previewImage.src = imageSrc
  }

  removePhoto() {
    const uploadArea = document.getElementById("uploadArea")
    const photoPreview = document.getElementById("photoPreview")
    const photoInput = document.getElementById("photoInput")

    uploadArea.style.display = "block"
    photoPreview.style.display = "none"
    photoInput.value = ""
    this.uploadedPhoto = null
    this.updateTryOnButton()
  }

  selectClothing(e) {
    const item = e.currentTarget
    const type = item.dataset.type
    const id = item.dataset.id

    // Remove selection from same category
    const categoryItems = document.querySelectorAll(`[data-type="${type}"]`)
    categoryItems.forEach((categoryItem) => {
      categoryItem.classList.remove("selected")
    })

    // Add selection to clicked item
    item.classList.add("selected")
    this.selectedClothing[type] = id

    this.updateTryOnButton()
  }

  updateTryOnButton() {
    const tryOnBtn = document.getElementById("tryOnBtn")
    const hasPhoto = this.uploadedPhoto !== null
    const hasClothing = Object.values(this.selectedClothing).some((item) => item !== null)

    tryOnBtn.disabled = !(hasPhoto && hasClothing)
  }

  async tryOnClothes() {
    const tryOnBtn = document.getElementById("tryOnBtn")
    const btnText = tryOnBtn.querySelector(".btn-text")
    const loadingSpinner = tryOnBtn.querySelector(".loading-spinner")

    // Show loading state
    btnText.textContent = "🤖 IA Processando..."
    loadingSpinner.style.display = "inline-block"
    tryOnBtn.disabled = true

    try {
      // Chamar API real do Django com IA
      const response = await this.callAITryOnAPI()

      if (response.success) {
        this.showResult(response.result_image_url, response.ai_analysis)
      } else {
        alert(`Erro da IA: ${response.error}`)
      }
    } catch (error) {
      console.error("Erro:", error)
      alert("Erro de conexão com a IA. Verifique sua internet e tente novamente.")
    } finally {
      // Reset button state
      btnText.textContent = "Experimentar Roupas"
      loadingSpinner.style.display = "none"
      tryOnBtn.disabled = false
    }
  }

  async callAITryOnAPI() {
    // Preparar dados para envio
    const formData = new FormData()
    formData.append("photo", this.uploadedPhoto)
    formData.append("clothing", JSON.stringify(this.selectedClothing))

    console.log("🚀 Enviando para IA:", this.selectedClothing)

    // Chamar API real do Django
    const response = await fetch("http://localhost:8000/api/try-on/", {
      method: "POST",
      body: formData,
    })

    const result = await response.json()
    console.log("🤖 Resposta da IA:", result)

    return result
  }

  showResult(resultImageUrl, aiAnalysis) {
    const resultSection = document.getElementById("resultSection")
    const resultImage = document.getElementById("resultImage")

    resultImage.src = resultImageUrl
    resultSection.style.display = "block"

    // Mostrar informações da análise da IA
    if (aiAnalysis) {
      console.log("📊 Análise da IA:", aiAnalysis)

      // Criar elemento para mostrar dados da IA
      let aiInfo = document.getElementById("aiAnalysisInfo")
      if (!aiInfo) {
        aiInfo = document.createElement("div")
        aiInfo.id = "aiAnalysisInfo"
        aiInfo.className = "ai-analysis-info"
        resultSection.appendChild(aiInfo)
      }

      aiInfo.innerHTML = `
        <h3>🤖 Análise da IA</h3>
        <p>✅ Pontos corporais detectados: ${aiAnalysis.landmarks_count}</p>
        <p>📏 Medidas calculadas: ${Object.keys(aiAnalysis.measurements).length}</p>
        <p>👤 Rosto detectado: ${aiAnalysis.face_detected ? "Sim" : "Não"}</p>
      `
    }

    // Scroll to result
    resultSection.scrollIntoView({ behavior: "smooth" })
  }

  tryAgain() {
    const resultSection = document.getElementById("resultSection")
    resultSection.style.display = "none"

    // Remover info da IA
    const aiInfo = document.getElementById("aiAnalysisInfo")
    if (aiInfo) {
      aiInfo.remove()
    }

    // Scroll back to top
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  saveResult() {
    const resultImage = document.getElementById("resultImage")
    const link = document.createElement("a")
    link.download = "mirrorfit-ai-resultado.png"
    link.href = resultImage.src
    link.click()
  }
}

// Initialize the app when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 MirrorFit com IA inicializado!")
  new MirrorFitApp()
})
