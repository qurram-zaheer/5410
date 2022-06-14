import logo from './logo.svg';
import './App.css';

import { Box, Button, Center, Stack, TextInput } from '@mantine/core';
import { SegmentedControl } from '@mantine/core';
import { useState, useEffect } from 'react';
import { useForm } from '@mantine/form';
import { useLocalStorage } from '@mantine/hooks';
import { Text } from '@mantine/core';
import axios from 'axios'

const registerService = axios.create({ baseURL: "https://container1-fj5lmilzfq-uc.a.run.app" })
const loginService = axios.create({ baseURL: "https://container2-fj5lmilzfq-uc.a.run.app" })
const sessionService = axios.create({ baseURL: "https://container3-fj5lmilzfq-uc.a.run.app" })

function App() {
  const [lsUser, setLsUser] = useLocalStorage({ key: "user", defaultValue: null })
  const [sessions, setSessions] = useState([])
  const [registerError, setRegisterError] = useState('')
  const [loginError, setLoginError] = useState('')
  const [logoutError, setLogoutError] = useState('')


  useEffect(() => {
    const getSessions = async () => {
      const res = await sessionService.get(`/sessions?user_id=${lsUser?.user_id}`).then(res => res.data)
      setSessions(res.data)
    }
    getSessions()
  }, [setSessions, loginError, logoutError])

  

  const registrationForm = useForm({
    initialValues: {
      email: '',
      password: '',
      name: '',
      location: ''
    },
  });

  const loginForm = useForm({
    initialValues: {
      email: '',
      password: '',
    },
  });

  const fireRegister = async (details) => {
    const res = await registerService.post("/register", details).then(res=>res.data)
    setRegisterError(res)
    registrationForm.reset()
  }

  const fireLogin = async (details) => {
    const res = await loginService.post("/login", details).then(res=>res.data)
    setLoginError(res)
    if (res.success){
      setLsUser({...details, user_id: res.user_id})
    }
    loginForm.reset()
  }

  const fireLogout = async () => {
    const res = await sessionService.post("/logout", {user_id: lsUser.user_id}).then(res=>res.data)
    if (res.success){
      setLsUser(null)
    }
    setLogoutError(res)
  }


  return (
    <div className="App">
      <Center style={{ 'height': '100vh' }}>
        <Stack>
          <Text size='xl'>Register</Text>
          <Box>
            <form onSubmit={registrationForm.onSubmit((values) => fireRegister(values))}>
              <TextInput
                required
                label="Name"
                placeholder="John doe"
                {...registrationForm.getInputProps('name')}
              />
              <TextInput
                required
                label="Email"
                placeholder="your@email.com"
                {...registrationForm.getInputProps('email')}
              />
              <TextInput
                required
                label="Password"
                placeholder="Enter a strong password"
                {...registrationForm.getInputProps('password')}
              />
              <TextInput
                required
                label="Location"
                placeholder="Paris"
                {...registrationForm.getInputProps('location')}
              />
              <Button type="submit" style={{ "marginTop": "10px" }}>Submit</Button>
              {registerError ? <Text size='sm' style={{ "marginTop": "5px" }} color={registerError.error ? "red" : "green"}>{registerError.error ? registerError.error : registerError.success}</Text> : null}
            </form>
          </Box>
        </Stack>
        <Stack style={{ marginLeft: "50px" }}>
          <Text size='xl'>Login</Text>
          <Box>
            <form onSubmit={loginForm.onSubmit((values) => fireLogin(values))}>
              <TextInput
                required
                label="Email"
                placeholder="your@email.com"
                {...loginForm.getInputProps('email')}
              />
              <TextInput
                required
                label="Password"
                placeholder="Password..."
                {...loginForm.getInputProps('password')}
              />
              <Button type="submit" style={{ "marginTop": "10px" }}>Submit</Button>
              {loginError ? <Text size='sm' style={{ "marginTop": "5px" }} color={loginError.error ? "red" : "green"}>{loginError.error ? loginError.error : loginError.success}</Text> : null}
            </form>
          </Box>
        </Stack>

        <Stack style={{ marginLeft: "50px", textAlign: "left" }}>
          {lsUser ? <Text color='green'>Hi {lsUser.email}, you are logged in</Text>:null}
          {lsUser ? <Button onClick = {fireLogout}>Logout</Button>:null}
          {logoutError.error ? <Text size='sm' style={{ "marginTop": "5px" }} color={logoutError.error ? "red" : "green"}>{logoutError.error ? logoutError.error : logoutError.success}</Text> : null}
          <Text size='xl'>Here are other users who are online:</Text>
          {sessions ? sessions.map(session => <div key={session.user}>
            <Text>{session.user}, since {new Date(session.timestamp*1000).toLocaleTimeString('en-US')} {new Date(session.timestamp*1000).toLocaleDateString('en-US')}</Text>
          </div>) : null}
        </Stack>
      </Center>
    </div>
  );
}

export default App;
