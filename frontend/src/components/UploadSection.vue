<template>
  <div class="upload-wrap">
    <div class="upload-box" :class="{ dragging, loaded: fileName }" @dragover.prevent="dragging=true" @dragleave="dragging=false" @drop.prevent="onDrop">
      <div v-if="!fileName" class="upload-idle">
        <div class="upload-icon">⬡</div>
        <p class="upload-title">Drop your CSV here</p>
        <p class="upload-sub">or click to browse</p>
        <input type="file" accept=".csv" @change="onFileChange" class="file-input" />
      </div>
      <div v-else class="upload-loaded">
        <span class="file-badge">✓ {{ fileName }}</span>
        <button class="reset-btn" @click="reset">✕ Reset</button>
      </div>
    </div>

    <div class="upload-hint">
      <p>CSV should have columns like: <span class="hint-tag">name</span> <span class="hint-tag">age</span> <span class="hint-tag">category</span> <span class="hint-tag">spend</span></p>
    </div>

    <button class="analyze-btn" :disabled="!file || loading" @click="analyze">
      <span v-if="loading" class="spinner">◌</span>
      <span v-else>Analyze →</span>
    </button>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  emits: ['data-analyzed'],
  data() {
    return { file: null, fileName: null, dragging: false, loading: false, error: null }
  },
  methods: {
    onFileChange(e) { this.setFile(e.target.files[0]) },
    onDrop(e) { this.setFile(e.dataTransfer.files[0]) },
    setFile(f) { if (f && f.name.endsWith('.csv')) { this.file = f; this.fileName = f.name; this.error = null } else { this.error = 'Please upload a .csv file' } },
    reset() { this.file = null; this.fileName = null },
    async analyze() {
      this.loading = true; this.error = null
      try {
        const form = new FormData()
        form.append('file', this.file)
        const res = await axios.post('https://datalens-backend-soxd.onrender.com', form)
        this.$emit('data-analyzed', res.data)
      } catch (e) {
        this.error = 'Analysis failed. Make sure backend is running on port 8000.'
      } finally { this.loading = false }
    }
  }
}
</script>

<style scoped>
.upload-wrap { display: flex; flex-direction: column; align-items: center; gap: 16px; }

.upload-box {
  width: 100%; max-width: 560px; border: 2px dashed var(--border);
  border-radius: 16px; padding: 48px 32px; text-align: center;
  position: relative; cursor: pointer; transition: all 0.2s;
  background: var(--surface);
}
.upload-box:hover, .upload-box.dragging { border-color: var(--accent); background: #16162a; }
.upload-box.loaded { border-style: solid; border-color: var(--accent3); }

.upload-icon { font-size: 40px; color: var(--accent); margin-bottom: 12px; }
.upload-title { font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 700; margin-bottom: 6px; }
.upload-sub { color: var(--text-muted); font-size: 13px; }
.file-input { position: absolute; inset: 0; opacity: 0; cursor: pointer; width: 100%; height: 100%; }

.upload-loaded { display: flex; align-items: center; gap: 16px; justify-content: center; }
.file-badge { background: #0d2e2a; color: var(--accent3); padding: 8px 16px; border-radius: 8px; font-size: 14px; }
.reset-btn { background: none; border: 1px solid var(--border); color: var(--text-muted); padding: 8px 14px; border-radius: 8px; cursor: pointer; }

.upload-hint { color: var(--text-muted); font-size: 12px; }
.hint-tag { background: var(--surface2); padding: 2px 8px; border-radius: 4px; color: var(--accent); margin: 0 2px; font-size: 11px; }

.analyze-btn {
  background: var(--accent); color: white; border: none; padding: 14px 40px;
  border-radius: 10px; font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 700;
  cursor: pointer; transition: all 0.2s; letter-spacing: 0.5px;
}
.analyze-btn:hover:not(:disabled) { background: #9b8fff; transform: translateY(-1px); }
.analyze-btn:disabled { opacity: 0.4; cursor: not-allowed; }

.spinner { display: inline-block; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.error { color: #ff4d6d; font-size: 13px; }
</style>