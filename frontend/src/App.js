import React from 'react';
import './App.css';
import { Button, Card, Form } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const BASE_API_URL = process.env.API_HOST || "http://localhost:5000";


function Stats({ info }) {
  return (
    <div
      className="info"
    >
      <span>{info.label}</span> {info.amt}
    </div>
  );
}

function FormGenerate({ generateObjects }) {

  const handleSubmit = e => {
    e.preventDefault();
    generateObjects();
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Button variant="primary mb-3" type="submit">
        Generate
    </Button>
    </Form>
  );
}

function FormReport({ reporter, task }) {

  const handleSubmit = e => {
    e.preventDefault();
    reporter(task.id);
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Button variant="secondary mb-3" type="submit">
        Report
    </Button>
    </Form>
  );
}

function App() {


  const [error, setError] = React.useState(null);
  const [task, setTask] = React.useState(null);
  const [items, setItems] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(false);


  const generateObjects = () => {
    const apiEndpoint = `${BASE_API_URL}/api/v1/random/generate`;
    setIsLoading(true);
    setItems([]);
    setTask(null);
    fetch(apiEndpoint).then(res => res.json())
      .then(
        (result) => {
          setIsLoading(false);
          const id = result.id;
          const url = `${BASE_API_URL}${result.path}`;
          setTask({
            'id': id,
            'url': url
          });
        },
        (error) => {
          setIsLoading(false);
          setError(error);
        }
      )
  };

  const reporter = (id) => {
    const apiEndpoint = `${BASE_API_URL}/api/v1/report/${id}`;
    fetch(apiEndpoint).then(res => res.json())
      .then(
        (result) => {
          setItems(result.items);
        },
        (error) => {
          setError(error);
        }
      )
  };

  return (
    <div className="app">
      <div className="container">
        <h1 className="text-center mb-4">Generate Random Objects</h1>
        <FormGenerate generateObjects={generateObjects} />

        {error &&
          <div>Error: {error.message}</div>
        }

        {isLoading &&
          <p>Loading...</p>
        }

        {task &&
          <div className="alert alert-success">
            <p>
              Link: <a href={task.url} target="_blank" rel="noopener noreferrer">Report link</a>
            </p>
            <FormReport reporter={reporter} task={task} />
          </div>
        }

        <div>
          {items.map((item, index) => (
            <Card key={index}>
              <Card.Body>
                <Stats
                  key={index}
                  info={item}
                />
              </Card.Body>
            </Card>
          ))}
        </div>

      </div>
    </div >
  );
}

export default App;
