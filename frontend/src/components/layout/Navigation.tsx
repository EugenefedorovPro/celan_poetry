import React from "react";
import { Navbar, Nav } from "react-bootstrap";
import logoPath from "../layout/celan.png";

export const Navigation: React.FC = () => {
    const isAuth = Boolean(localStorage.getItem("access_token"));

    return (
        <Navbar bg="dark" variant="dark" className="py-0">
            <Navbar.Brand href="/" className="pb-0">
                <img
                    src={logoPath}
                    alt="Paul Celan"
                    width={50}
                    height={40}
                />
            </Navbar.Brand>

            <Nav className="ms-auto">
                {isAuth ? (
                    <Nav.Link href="/logout">Logout</Nav.Link>
                ) : (
                    <>
                        <Nav.Link href="/login">Login</Nav.Link>
                        <Nav.Link href="/signup">Signup</Nav.Link>
                    </>
                )}
            </Nav>
        </Navbar>
    );
};
