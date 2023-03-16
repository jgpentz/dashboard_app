import './App.css';
import { ChakraProvider } from '@chakra-ui/react'
import { Main } from './views/Main';

function App() {
  return (
    <ChakraProvider>
      <div className="App">
        <Main />
      </div>
    </ChakraProvider>
  );
}

export default App;
