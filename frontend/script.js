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
    this.testAIConnection()
  }

  async testAIConnection() {
    try {
      const response = await fetch("http://localhost:8000/api/health/")
      const data = await response.json()

      if (data.status === "OK") {
        console.log("✅ Backend conectado:", data.message)
        console.log("🤖 Status da IA:", data.ai_status)

        if (data.ai_status.includes("✅")) {
          this.showStatus("🤖 IA Real carregada e funcionando!", "success")
        } else {
          this.showStatus("⚠️ IA com problemas. Instale dependências: pip install opencv-python mediapipe", "warning")
        }
      }
    } catch (error) {
      console.log("⚠️ Backend não conectado:", error)
      this.showStatus("❌ Backend não está rodando. Execute: python manage.py runserver", "error")
    }
  }

  showStatus(message, type) {
    let statusEl = document.getElementById("connectionStatus")
    if (!statusEl) {
      statusEl = document.createElement("div")
      statusEl.id = "connectionStatus"
      statusEl.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 12px;
        font-weight: 600;
        z-index: 1000;
        transition: all 0.3s ease;
        max-width: 400px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
      `
      document.body.appendChild(statusEl)
    }

    statusEl.textContent = message

    if (type === "success") {
      statusEl.style.background = "linear-gradient(135deg, #d4edda, #c3e6cb)"
      statusEl.style.color = "#155724"
      statusEl.style.border = "2px solid #28a745"
    } else if (type === "warning") {
      statusEl.style.background = "linear-gradient(135deg, #fff3cd, #ffeaa7)"
      statusEl.style.color = "#856404"
      statusEl.style.border = "2px solid #ffc107"
    } else if (type === "error") {
      statusEl.style.background = "linear-gradient(135deg, #f8d7da, #f5c6cb)"
      statusEl.style.color = "#721c24"
      statusEl.style.border = "2px solid #dc3545"
    }

    // Auto hide after 8 seconds
    setTimeout(() => {
      if (statusEl) {
        statusEl.style.opacity = "0"
        setTimeout(() => statusEl.remove(), 300)
      }
    }, 8000)
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

    if (file.size > 10 * 1024 * 1024) {
      alert("O arquivo deve ter no máximo 10MB.")
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      this.uploadedPhoto = file
      this.showPhotoPreview(e.target.result)
      this.updateTryOnButton()
      this.showStatus("📸 Foto carregada! Agora selecione roupas e clique em 'Experimentar'", "success")
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

    // Show feedback
    const itemName = item.querySelector(".clothing-name").textContent
    this.showStatus(`✅ ${itemName} selecionado!`, "success")
  }

  updateTryOnButton() {
    const tryOnBtn = document.getElementById("tryOnBtn")
    const hasPhoto = this.uploadedPhoto !== null
    const hasClothing = Object.values(this.selectedClothing).some((item) => item !== null)

    tryOnBtn.disabled = !(hasPhoto && hasClothing)

    if (hasPhoto && hasClothing) {
      tryOnBtn.style.opacity = "1"
      tryOnBtn.style.cursor = "pointer"
      tryOnBtn.querySelector(".btn-text").textContent = "🤖 Experimentar com IA Real"
    } else {
      tryOnBtn.style.opacity = "0.6"
      tryOnBtn.style.cursor = "not-allowed"
      tryOnBtn.querySelector(".btn-text").textContent = "Carregue foto e selecione roupas"
    }
  }

  async tryOnClothes() {
    const tryOnBtn = document.getElementById("tryOnBtn")
    const btnText = tryOnBtn.querySelector(".btn-text")
    const loadingSpinner = tryOnBtn.querySelector(".loading-spinner")

    // Show loading state
    btnText.textContent = "🤖 IA Processando..."
    loadingSpinner.style.display = "inline-block"
    tryOnBtn.disabled = true

    // Show processing status
    this.showStatus("🔄 IA analisando sua foto e aplicando roupas...", "success")

    try {
      const response = await this.callTryOnAPI()

      if (response.success) {
        this.showResult(response)
        this.showStatus("🎉 Processamento com IA concluído!", "success")
      } else {
        this.showStatus(`❌ Erro da IA: ${response.error}`, "error")
        alert(`Erro da IA: ${response.error}`)
      }
    } catch (error) {
      console.error("Erro:", error)
      this.showStatus("❌ Erro de conexão. Verifique se o backend está rodando.", "error")
      alert("Erro de conexão. Verifique se o backend Django está rodando.")
    } finally {
      // Reset button state
      btnText.textContent = "🤖 Experimentar com IA Real"
      loadingSpinner.style.display = "none"
      this.updateTryOnButton()
    }
  }

  async callTryOnAPI() {
    const formData = new FormData()
    formData.append("photo", this.uploadedPhoto)
    formData.append("clothing", JSON.stringify(this.selectedClothing))

    console.log("🚀 Enviando para IA:", this.selectedClothing)

    const response = await fetch("http://localhost:8000/api/try-on/", {
      method: "POST",
      body: formData,
    })

    const result = await response.json()
    console.log("🤖 Resposta da IA:", result)

    return result
  }

  showResult(response) {
    const resultSection = document.getElementById("resultSection")
    const resultImage = document.getElementById("resultImage")

    // Mostrar imagem processada pela IA
    resultImage.src = response.result_image_url
    resultSection.style.display = "block"

    // Mostrar informações da IA
    let aiInfo = document.getElementById("aiAnalysisInfo")
    if (!aiInfo) {
      aiInfo = document.createElement("div")
      aiInfo.id = "aiAnalysisInfo"
      aiInfo.className = "ai-analysis-info"
      aiInfo.style.cssText = `
        background: linear-gradient(135deg, #e6f3ff 0%, #f0f8ff 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 25px 0;
        border: 2px solid #dfbd87;
        box-shadow: 0 8px 25px rgba(223, 189, 135, 0.2);
      `
      resultSection.appendChild(aiInfo)
    }

    const analysis = response.ai_analysis
    aiInfo.innerHTML = `
      <h3 style="color: #2c2c2c; margin-bottom: 15px;">🤖 Análise da IA Real</h3>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
        <div>
          <strong>🎯 Pontos Corporais:</strong><br>
          ${analysis.body_landmarks_detected} pontos detectados
        </div>
        <div>
          <strong>👤 Rosto:</strong><br>
          ${analysis.face_detected ? "✅ Detectado" : "❌ Não detectado"}
        </div>
        <div>
          <strong>👕 Roupas Aplicadas:</strong><br>
          ${analysis.applied_items.join(", ")}
        </div>
        <div>
          <strong>🔧 Método:</strong><br>
          ${analysis.processing_method}
        </div>
      </div>
      <p style="margin-top: 15px; font-style: italic; color: #666;">
        ✨ Sua foto foi processada com IA real usando MediaPipe para detecção corporal e OpenCV para aplicação de roupas!
      </p>
    `

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

    this.showStatus("💾 Resultado da IA salvo!", "success")
  }
}

// Initialize the app when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 MirrorFit com IA Real inicializado!")
  window.mirrorFitApp = new MirrorFitApp()
})
