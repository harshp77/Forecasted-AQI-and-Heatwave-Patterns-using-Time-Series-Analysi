import React from 'react'
import { ToggleButton, FormControl, MenuItem, Select, InputLabel } from '@mui/material'
import { ToggleButtonGroup } from '@mui/material'
import {BsThermometerHalf} from 'react-icons/bs'
import { RiWindyLine } from 'react-icons/ri'
// BsThermometerHalf
const Home = () => {

  const [output, setOutput] = React.useState('')

  const handelChange = ()=>{

  }

  return (
    <div className='flex flex-col mt-8'>
      <div className='flex justify-between items-center'>
        <ToggleButtonGroup
          value={output}
          exclusive
          onChange={handelChange}
          aria-label='Output'
          className='h-12 bg-cta w-max'
          size='large'
        >
          <ToggleButton value='AQI'>
            <BsThermometerHalf className='w-20' title='AQI' size={30} color='white'/>
          </ToggleButton>
          <ToggleButton value='HeatWave'>
            <RiWindyLine className='w-20' title='Heat Wave' size={30} color='white'/>
          </ToggleButton>
        </ToggleButtonGroup>
        
        <FormControl variant='standard' sx={{ m: 1, minWidth: 200 }}>
          <InputLabel id='demo-simple-select-standard-label'>City</InputLabel>
          <Select
            labelId='demo-simple-select-standard-label'
            id='demo-simple-select-standard'
            value={10}
            label='Age'
          >
            <MenuItem value={1}>Ten</MenuItem>
            <MenuItem value={2}>Ten</MenuItem>
            <MenuItem value={3}>Ten</MenuItem>
            <MenuItem value={4}>Ten</MenuItem>
            <MenuItem value={5}>Ten</MenuItem>
          </Select>
        </FormControl>
        <FormControl variant='standard' sx={{ m: 1, minWidth: 200 }}>
          <InputLabel id='demo-simple-select-standard-label'>Month</InputLabel>
          <Select
            labelId='demo-simple-select-standard-label'
            id='demo-simple-select-standard'
            value={10}
            label='Age'
          >
            <MenuItem value={1}>January</MenuItem>
            <MenuItem value={2}>February</MenuItem>
            <MenuItem value={3}>March</MenuItem>
            <MenuItem value={4}>April</MenuItem>
            <MenuItem value={5}>May</MenuItem>
            <MenuItem value={6}>June</MenuItem>
            <MenuItem value={7}>July</MenuItem>
            <MenuItem value={8}>August</MenuItem>
            <MenuItem value={9}>September</MenuItem>
            <MenuItem value={10}>October</MenuItem>
            <MenuItem value={11}>November</MenuItem>
            <MenuItem value={12}>December</MenuItem>
          </Select>
        </FormControl>
      </div>
    </div>
  )
}

export default Home