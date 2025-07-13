describe('R8UC1 to R8UC3)', () => {
  let user;

  before(() => {
    return cy.fixture('user.json').then((data) => {
      user = data;

      return cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user,
      }).then((res) => {
        user._id = res.body._id.$oid;
      });
    });
  });


  beforeEach(() => {
    cy.visit('http://localhost:3000');

    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(user.email);

    cy.get('form').submit();

    cy.contains(`Your tasks, ${user.firstName} ${user.lastName}`, { timeout: 8000 }).should('exist');
  });


  it('R8UC1: Add', () => {
    cy.get('#title').type('Test task for R8UC1');
    cy.get('#url').type('x7X9w_GIm1s');
    cy.get('input[type="submit"][value="Create new Task"]').click();
    cy.contains('.title-overlay', 'Test task for R8UC1').click();
    cy.get('input[placeholder="Add a new todo item"]')
      .type('Watch video{enter}');

    cy.contains('.todo-item', 'Watch video').should('exist');
  });


  it('R8UC2: Toggle', () => {
    cy.get('#title').type('Test task for R8UC2');
    cy.get('#url').type('url-toggle');
    cy.get('input[type="submit"][value="Create new Task"]').click();
    cy.contains('.title-overlay', 'Test task for R8UC2').click();
    cy.get('input[placeholder="Add a new todo item"]')
      .type('Watch video{enter}');

    cy.contains('.todo-item', 'Watch video')
      .find('.checker')
      .click({ force: true });

    cy.contains('.todo-item', 'Watch video')
      .find('.checker')
      .should('have.class', 'checked');

    cy.contains('.todo-item', 'Watch video')
      .find('.checker')
      .click({ force: true });

    cy.contains('.todo-item', 'Watch video')
      .find('.checker')
      .should('have.class', 'unchecked');
  });

  it('R8UC3: Delete', () => {
    cy.get('#title').type('Test task for R8UC3');
    cy.get('#url').type('url-delete');
    cy.get('input[type="submit"][value="Create new Task"]').click();
    cy.contains('.title-overlay', 'Test task for R8UC3', { timeout: 8000 }).click();
    cy.contains('.todo-item', 'Watch video', { timeout: 8000 }).should('exist');
    cy.contains('.todo-item', 'Watch video')
      .find('.checker')
      .click({ force: true });

    cy.contains('.todo-item', 'Watch video')
      .find('.remover')
      .click({ force: true });

    cy.contains('.todo-item', 'Watch video').should('not.exist');
  });

  after(() => {
    cy.request('DELETE', `http://localhost:5000/users/${user._id}`);
  });
});
