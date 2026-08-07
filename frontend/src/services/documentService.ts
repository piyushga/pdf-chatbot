export type DocumentResponse = {
  document_id: string
  file_name: string
  file_hash: string
  file_size: number
  status: 'uploaded' | 'processing' | 'ready' | 'failed'
  uploaded_at: string
}

const API_BASE_URL = 'http://127.0.0.1:8001/api'

export async function uploadDocument(file: File): Promise<DocumentResponse> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE_URL}/documents`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const error = (await response.json()) as { detail?: string }
    throw new Error(error.detail ?? 'PDF upload failed.')
  }

  return response.json() as Promise<DocumentResponse>
}
