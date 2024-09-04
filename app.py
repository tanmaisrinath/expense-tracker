import streamlit as st


with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

home_page = st.Page(
    page="views/home_page.py", title="Home", icon=":material/home:", default=True
)
add_expense_page = st.Page(
    page="views/add_expense.py", title="Add Expense", icon=":material/add:"
)
view_expenses_page = st.Page(
    page="views/view_expenses.py", title="View Expenses", icon=":material/visibility:"
)


pg = st.navigation(pages=[home_page, add_expense_page, view_expenses_page])
pg.run()
