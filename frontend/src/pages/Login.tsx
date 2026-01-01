// src/pages/Login.tsx
import React, { useState } from "react";
import { login } from "../api/auth";
import {
  Button,
  Card,
  CardBody,
  Container,
  Form,
  FormControl,
  FormGroup,
  FormLabel,
} from "react-bootstrap";

export const Login = () => {
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState("");

  const submit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    await login(username, password);

    // interceptor will handle auth headers automatically
    window.location.href = "/";
  };

  return (
    <Container className="d-flex justify-content-center mt-5">
      <Card>
        <CardBody>
          <Form onSubmit={submit}>
            <FormGroup>
              <FormLabel>Username</FormLabel>
              <FormControl
                className="mt-1"
                placeholder="Enter Username"
                type="text"
                required
                onChange={(e) => setUserName(e.target.value)}
              />
            </FormGroup>

            <FormGroup className="mt-3">
              <FormLabel>Password</FormLabel>
              <FormControl
                className="mt-1"
                placeholder="Enter Password"
                type="password"
                required
                onChange={(e) => setPassword(e.target.value)}
              />
              <div className="d-grid gap-2 mt-3">
                <Button type="submit">Submit</Button>
              </div>
            </FormGroup>
          </Form>
        </CardBody>
      </Card>
    </Container>
  );
};
