import express from 'express';

const app = express();
app.use(express.json());

// Mock: Create user
app.post('/users/create', (req, res) => {
  res.json({ _id: { $oid: 'mock-user-id-123' } });
});

// Mock: Delete user
app.delete('/users/:id', (req, res) => {
  res.send({ deleted: true });
});

app.listen(5000, () => {
  console.log('✅ Backend running on http://localhost:5000');
});
