import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import Accordion from '@mui/material/Accordion'
import AccordionDetails from '@mui/material/AccordionDetails'
import AccordionSummary from '@mui/material/AccordionSummary'
import Typography from '@mui/material/Typography'
import * as React from 'react'

import RunStatusAppDetail from './RunStatusAppDetail'

interface RunStatusAppProps {
  panel: string
  expanded: string | false
  handleChange: (
    _panel: string
  ) => (_event: React.SyntheticEvent, _isExpanded: boolean) => void
}

export default function RunStatusApp({
  panel,
  expanded,
  handleChange
}: RunStatusAppProps) {
  return (
    <>
      <Accordion expanded={expanded === panel} onChange={handleChange(panel)}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls='panel1bh-content'
          id='panel1bh-header'
        >
          <Typography sx={{ width: '33%', flexShrink: 0 }}>
            {'{date}'}
          </Typography>
          <Typography sx={{ color: 'text.secondary' }}>
            {'{project_name} - {publish_name}'}
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <RunStatusAppDetail />
        </AccordionDetails>
      </Accordion>
    </>
  )
}
