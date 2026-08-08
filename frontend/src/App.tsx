import { Box, Container, CssBaseline, Stack, Typography } from '@mui/material'
import { createTheme, ThemeProvider } from '@mui/material/styles'

import PdfUpload from './components/PdfUpload'

const theme = createTheme({
  palette: {
    primary: {
      main: '#4f46e5',
    },
    background: {
      default: '#f6f7fb',
    },
  },
  typography: {
    fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
  },
  shape: {
    borderRadius: 12,
  },
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        component="main"
        sx={{ minHeight: '100vh', py: { xs: 6, sm: 10 } }}
      >
        <Container maxWidth="sm">
          <Stack spacing={4}>
            <Stack spacing={1.5} sx={{ textAlign: 'center' }}>
              <Typography
                color="primary"
                sx={{ fontWeight: 700, letterSpacing: '0.08em' }}
              >
                AI PDF CHATBOT
              </Typography>
              <Typography component="h1" variant="h3" sx={{ fontWeight: 800 }}>
                Chat with your documents
              </Typography>
              <Typography color="text.secondary" sx={{ fontSize: '1.05rem' }}>
                Upload a PDF now. Text extraction and grounded chat are coming next.
              </Typography>
            </Stack>

            <PdfUpload />
          </Stack>
        </Container>
      </Box>
    </ThemeProvider>
  )
}

export default App
