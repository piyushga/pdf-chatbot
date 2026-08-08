import { useState, type ChangeEvent } from 'react'
import {
  Alert,
  Box,
  Button,
  LinearProgress,
  Paper,
  Stack,
  Typography,
} from '@mui/material'
import { styled } from '@mui/material/styles'

import {
  uploadDocument,
  type DocumentResponse,
} from '../services/documentService'

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
})

function PdfUpload() {
  const [uploadedDocument, setUploadedDocument] =
    useState<DocumentResponse | null>(null)
  const [errorMessage, setErrorMessage] = useState('')
  const [isUploading, setIsUploading] = useState(false)

  async function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    event.target.value = ''

    if (!file) return

    setIsUploading(true)
    setErrorMessage('')
    setUploadedDocument(null)

    try {
      const document = await uploadDocument(file)
      setUploadedDocument(document)
    } catch (error) {
      const message =
        error instanceof Error ? error.message : 'PDF upload failed.'
      setErrorMessage(message)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <Paper variant="outlined" sx={{ borderRadius: 4, overflow: 'hidden' }}>
      {isUploading && <LinearProgress />}

      <Stack
        spacing={3}
        sx={{ alignItems: 'center', p: { xs: 3, sm: 5 } }}
      >
        <Box
          aria-hidden="true"
          sx={{
            display: 'grid',
            placeItems: 'center',
            width: 64,
            height: 64,
            borderRadius: '50%',
            bgcolor: 'primary.50',
            fontSize: 30,
          }}
        >
          ↑
        </Box>

        <Stack spacing={1} sx={{ textAlign: 'center' }}>
          <Typography component="h2" variant="h5" sx={{ fontWeight: 700 }}>
            Upload a PDF
          </Typography>
          <Typography color="text.secondary">
            Choose one PDF up to 20 MB. Upload starts automatically.
          </Typography>
        </Stack>

        <Button
          component="label"
          variant="contained"
          size="large"
          disabled={isUploading}
        >
          {isUploading ? 'Uploading…' : 'Choose PDF'}
          <VisuallyHiddenInput
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileChange}
          />
        </Button>

        <Box sx={{ width: '100%' }} aria-live="polite">
          {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
          {uploadedDocument && (
            <Alert severity="success">
              <strong>{uploadedDocument.file_name}</strong> uploaded successfully.
            </Alert>
          )}
        </Box>
      </Stack>
    </Paper>
  )
}

export default PdfUpload
