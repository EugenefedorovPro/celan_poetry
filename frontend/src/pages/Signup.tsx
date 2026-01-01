import React, { useState } from "react";
import AxiosInstance from "../api/http";
import type { AxiosError, AxiosResponse } from "axios";
import { Button, Col, Container, Form, Row } from "react-bootstrap";

interface ErrorsData {
  username?: string[];
  password?: string[];
  password2?: string[];
  email?: string[];
  first_name?: string[];
  last_name?: string[];
  non_field_errors?: string[];
  detail?: string;
}

export const Signup: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [errors, setErrors] = useState<ErrorsData | null>(null);

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = async (
    event
  ) => {
    event.preventDefault();
    setErrors(null);

    try {
      const response: AxiosResponse = await AxiosInstance.post(
        "/signup/",
        {
          username,
          password,
          password2,
          email,
          first_name: firstName,
          last_name: lastName,
        },
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      console.log(response.status);
      console.log(response.data);

      // Optional: redirect after successful signup
      // window.location.replace("/login");
    } catch (err) {
      const error = err as AxiosError<ErrorsData>;
      console.error(error);

      // If backend sent validation errors, show them; otherwise show generic
      setErrors(error.response?.data ?? { detail: "Signup failed" });
    }
  };

  const handleChange: React.ChangeEventHandler<HTMLInputElement> = (event) => {
    const { name, value } = event.target;

    switch (name) {
      case "username":
        setUsername(value);
        break;
      case "password":
        setPassword(value);
        break;
      case "password2":
        setPassword2(value);
        break;
      case "email":
        setEmail(value);
        break;
      case "first_name":
        setFirstName(value);
        break;
      case "last_name":
        setLastName(value);
        break;
      default:
        break;
    }
  };

  return (
    <Container>
      <Row>
        <Col className="mt-3 d-flex justify-content-center align-items-center">
          <Form onSubmit={handleSubmit}>
            <h3 className="mb-4">Create your account</h3>

            {errors?.detail && (
              <div className="text-danger mb-2">{errors.detail}</div>
            )}
            {errors?.non_field_errors?.length ? (
              <div className="text-danger mb-2">
                {errors.non_field_errors.join(", ")}
              </div>
            ) : null}

            <Form.Group className="mb-2">
              <Form.Label>Username</Form.Label>
              <Form.Control
                name="username"
                type="text"
                value={username}
                onChange={handleChange}
                isInvalid={!!errors?.username?.length}
                required
              />
              <Form.Control.Feedback type="invalid">
                <ul className="mb-0">
                  {errors?.username?.map((e, i) => (
                    <li key={i}>{e}</li>
                  ))}
                </ul>
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-2">
              <Form.Label>Password</Form.Label>
              <Form.Control
                name="password"
                type="password"
                value={password}
                onChange={handleChange}
                isInvalid={!!errors?.password?.length}
                required
              />
              <Form.Control.Feedback type="invalid">
                <ul className="mb-0">
                  {errors?.password?.map((e, i) => (
                    <li key={i}>{e}</li>
                  ))}
                </ul>
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-2">
              <Form.Label>Repeat password</Form.Label>
              <Form.Control
                name="password2"
                type="password"
                value={password2}
                onChange={handleChange}
                isInvalid={!!errors?.password2?.length}
                required
              />
              <Form.Control.Feedback type="invalid">
                <ul className="mb-0">
                  {errors?.password2?.map((e, i) => (
                    <li key={i}>{e}</li>
                  ))}
                </ul>
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-2">
              <Form.Label>Email</Form.Label>
              <Form.Control
                name="email"
                type="email"
                value={email}
                onChange={handleChange}
                isInvalid={!!errors?.email?.length}
              />
              <Form.Control.Feedback type="invalid">
                <ul className="mb-0">
                  {errors?.email?.map((e, i) => (
                    <li key={i}>{e}</li>
                  ))}
                </ul>
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-2">
              <Form.Label>First name</Form.Label>
              <Form.Control
                name="first_name"
                type="text"
                value={firstName}
                onChange={handleChange}
                isInvalid={!!errors?.first_name?.length}
              />
            </Form.Group>

            <Form.Group className="mb-2">
              <Form.Label>Last name</Form.Label>
              <Form.Control
                name="last_name"
                type="text"
                value={lastName}
                onChange={handleChange}
                isInvalid={!!errors?.last_name?.length}
              />
            </Form.Group>

            <Button type="submit" variant="primary" className="mt-3">
              Submit
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};
