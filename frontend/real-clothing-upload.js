// JavaScript para upload de roupas reais
class RealClothingUpload {
  constructor() {
    this.initializeRealClothingFeature()
  }

  initializeRealClothingFeature() {
    // Adicionar botão para upload de roupa real
    this.addRealClothingButton()

    // Event listeners
    document.getElementById("realClothingBtn")?.addEventListener("click", this.showRealClothingModal.bind(this))
  }

  addRealClothingButton() {
    const clothingSection = document.querySelector(".clothing-selection")
    if (!clothingSection) return

    // Adicionar botão antes das categorias
    const realClothingDiv = document.createElement("div")
    realClothingDiv.className = "real-clothing-section"
    realClothingDiv.innerHTML = `
            <div class="real-clothing-banner">
                <h3>🔥 Novo! Use suas próprias roupas</h3>
                <p>Faça upload de uma foto do seu Air Force 1, bermuda ou qualquer roupa e veja como fica em você!</p>
                <button id="realClothingBtn" class="real-clothing-btn">
                    📸 Upload de Roupa Real
                </button>
            </div>
        `

    clothingSection.insertBefore(realClothingDiv, clothingSection.firstChild)

    // Adicionar CSS
    this.addRealClothingStyles()
  }

  addRealClothingStyles() {
    const style = document.createElement("style")
    style.textContent = `
            .real-clothing-banner {
                background: linear-gradient(135deg, #ff6b6b, #ffa500);
                color: white;
                padding: 1.5rem;
                border-radius: 12px;
                text-align: center;
                margin-bottom: 2rem;
                box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
            }
            
            .real-clothing-banner h3 {
                margin-bottom: 0.5rem;
                font-size: 1.3rem;
            }
            
            .real-clothing-banner p {
                margin-bottom: 1rem;
                opacity: 0.9;
            }
            
            .real-clothing-btn {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid white;
                padding: 0.8rem 2rem;
                border-radius: 25px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .real-clothing-btn:hover {
                background: white;
                color: #ff6b6b;
                transform: translateY(-2px);
            }
            
            .real-clothing-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
            }
            
            .real-clothing-content {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                max-width: 500px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
            }
            
            .clothing-type-selector {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
                margin: 1rem 0;
            }
            
            .clothing-type-option {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 1rem;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .clothing-type-option:hover,
            .clothing-type-option.selected {
                border-color: #667eea;
                background: #f0f8ff;
            }
            
            .upload-area-real {
                border: 3px dashed #cbd5e0;
                border-radius: 10px;
                padding: 2rem;
                text-align: center;
                cursor: pointer;
                margin: 1rem 0;
                transition: all 0.3s ease;
            }
            
            .upload-area-real:hover {
                border-color: #667eea;
                background: #f8f9ff;
            }
        `
    document.head.appendChild(style)
  }

  showRealClothingModal() {
    const modal = document.createElement("div")
    modal.className = "real-clothing-modal"
    modal.innerHTML = `
            <div class="real-clothing-content">
                <h2>📸 Upload de Roupa Real</h2>
                <p>Envie uma foto da roupa que você quer experimentar virtualmente!</p>
                
                <div class="clothing-type-selector">
                    <div class="clothing-type-option" data-type="shoes">
                        <div>👟</div>
                        <p>Tênis</p>
                        <small>Air Force, Jordan, etc.</small>
                    </div>
                    <div class="clothing-type-option" data-type="shirt">
                        <div>👕</div>
                        <p>Camiseta</p>
                        <small>Qualquer camiseta</small>
                    </div>
                    <div class="clothing-type-option" data-type="pants">
                        <div>👖</div>
                        <p>Calça</p>
                        <small>Jeans, social, etc.</small>
                    </div>
                    <div class="clothing-type-option" data-type="shorts">
                        <div>🩳</div>
                        <p>Bermuda</p>
                        <small>Qualquer bermuda</small>
                    </div>
                </div>
                
                <div class="upload-area-real" id="realClothingUpload">
                    <div>📷</div>
                    <p>Clique para enviar foto da roupa</p>
                    <small>JPG, PNG (máx. 5MB)</small>
                    <input type="file" id="realClothingInput" accept="image/*" hidden>
                </div>
                
                <input type="text" id="clothingName" placeholder="Nome da roupa (ex: Air Force 1 Branco)" 
                       style="width: 100%; padding: 0.8rem; margin: 1rem 0; border: 1px solid #ddd; border-radius: 8px;">
                
                <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                    <button id="cancelRealClothing" class="btn-secondary" style="flex: 1;">Cancelar</button>
                    <button id="processRealClothing" class="btn-primary" style="flex: 1;" disabled>
                        🤖 Processar com IA
                    </button>
                </div>
            </div>
        `

    document.body.appendChild(modal)

    // Event listeners do modal
    this.setupModalEventListeners(modal)
  }

  setupModalEventListeners(modal) {
    let selectedType = null
    let selectedFile = null

    // Seleção de tipo de roupa
    modal.querySelectorAll(".clothing-type-option").forEach((option) => {
      option.addEventListener("click", () => {
        modal.querySelectorAll(".clothing-type-option").forEach((opt) => opt.classList.remove("selected"))
        option.classList.add("selected")
        selectedType = option.dataset.type
        this.updateProcessButton(modal, selectedType, selectedFile)
      })
    })

    // Upload de arquivo
    const uploadArea = modal.querySelector("#realClothingUpload")
    const fileInput = modal.querySelector("#realClothingInput")

    uploadArea.addEventListener("click", () => fileInput.click())

    fileInput.addEventListener("change", (e) => {
      const file = e.target.files[0]
      if (file) {
        selectedFile = file
        uploadArea.innerHTML = `
                    <div>✅</div>
                    <p>Foto carregada: ${file.name}</p>
                    <small>Clique para trocar</small>
                `
        this.updateProcessButton(modal, selectedType, selectedFile)
      }
    })

    // Botões
    modal.querySelector("#cancelRealClothing").addEventListener("click", () => {
      document.body.removeChild(modal)
    })

    modal.querySelector("#processRealClothing").addEventListener("click", () => {
      const clothingName = modal.querySelector("#clothingName").value || "Roupa personalizada"
      this.processRealClothing(selectedFile, selectedType, clothingName, modal)
    })

    // Fechar ao clicar fora
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        document.body.removeChild(modal)
      }
    })
  }

  updateProcessButton(modal, type, file) {
    const processBtn = modal.querySelector("#processRealClothing")
    processBtn.disabled = !(type && file)
  }

  async processRealClothing(clothingFile, clothingType, clothingName, modal) {
    const processBtn = modal.querySelector("#processRealClothing")
    const originalText = processBtn.textContent

    processBtn.textContent = "🤖 IA Processando..."
    processBtn.disabled = true

    try {
      // Verificar se tem foto da pessoa
      if (!window.mirrorFitApp?.uploadedPhoto) {
        alert("Por favor, faça upload da sua foto primeiro!")
        return
      }

      // Preparar dados
      const formData = new FormData()
      formData.append("person_photo", window.mirrorFitApp.uploadedPhoto)
      formData.append("clothing_photo", clothingFile)
      formData.append("clothing_type", clothingType)
      formData.append("clothing_name", clothingName)

      console.log(`🚀 Processando ${clothingName} (${clothingType}) com IA...`)

      // Chamar API
      const response = await fetch("http://localhost:8000/api/real-clothing-tryon/", {
        method: "POST",
        body: formData,
      })

      const result = await response.json()

      if (result.success) {
        // Fechar modal
        document.body.removeChild(modal)

        // Mostrar resultado
        this.showRealClothingResult(result)
      } else {
        alert(`Erro da IA: ${result.error}`)
      }
    } catch (error) {
      console.error("Erro:", error)
      alert("Erro de conexão com a IA. Tente novamente.")
    } finally {
      processBtn.textContent = originalText
      processBtn.disabled = false
    }
  }

  showRealClothingResult(result) {
    const resultSection = document.getElementById("resultSection")
    const resultImage = document.getElementById("resultImage")

    resultImage.src = result.result_image_url
    resultSection.style.display = "block"

    // Adicionar informações da roupa real
    let realClothingInfo = document.getElementById("realClothingInfo")
    if (!realClothingInfo) {
      realClothingInfo = document.createElement("div")
      realClothingInfo.id = "realClothingInfo"
      realClothingInfo.className = "real-clothing-result-info"
      resultSection.appendChild(realClothingInfo)
    }

    realClothingInfo.innerHTML = `
            <div style="background: linear-gradient(135deg, #ff6b6b, #ffa500); color: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <h3>🔥 Roupa Real Aplicada!</h3>
                <p><strong>${result.clothing_info.name}</strong></p>
                <p>Tipo: ${this.getClothingTypeName(result.clothing_info.type)}</p>
                <p>✨ Processado com IA avançada</p>
            </div>
        `

    // Scroll para resultado
    resultSection.scrollIntoView({ behavior: "smooth" })

    console.log("🎉 Roupa real aplicada com sucesso!", result)
  }

  getClothingTypeName(type) {
    const names = {
      shoes: "Tênis",
      shirt: "Camiseta",
      pants: "Calça",
      shorts: "Bermuda",
    }
    return names[type] || type
  }
}

// Inicializar quando DOM carregar
document.addEventListener("DOMContentLoaded", () => {
  new RealClothingUpload()
})
