import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import Accordion from '@mui/material/Accordion'
import AccordionDetails from '@mui/material/AccordionDetails'
import AccordionSummary from '@mui/material/AccordionSummary'
import Typography from '@mui/material/Typography'
import * as React from 'react'

import { RunStatusAppProps } from '../../types/dashboard'
import formatDate from '../../utils/formatDate'
import RunStatusAppDetail from './RunStatusAppDetail'

export default function RunStatusApp({
  panel,
  expanded,
  handleChange,
  statusData
}: RunStatusAppProps) {
  return (
    <>
      <Accordion expanded={expanded} onChange={handleChange(panel)}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls='panel1bh-content'
          id='panel1bh-header'
        >
          <Typography sx={{ width: '23%', flexShrink: 0 }}>
            {formatDate(statusData.date)}
          </Typography>
          <Typography sx={{ width: '10%', flexShrink: 0 }}>
{statusData.project_name}
          </Typography>
          <Typography sx={{ color: 'text.secondary' }}>
            {statusData.article_title}
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <RunStatusAppDetail networkStatuses={statusData.network_statuses} />
        </AccordionDetails>
      </Accordion>
    </>
  )
}
